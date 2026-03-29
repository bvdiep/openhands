#!/home/dd/work/diep/openhands/apps/mcp_gen_img_vid_with_refs/.venv/bin/python
import os
import sys
import asyncio
import argparse
import shutil
import yaml
from pathlib import Path
from dotenv import load_dotenv
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

load_dotenv()

MCP_SERVER_PATH = str(Path(__file__).parent.parent / "mcp_gen_img_vid_with_refs" / "server.py")
MCP_VENV_PYTHON = str(Path(__file__).parent.parent / "mcp_gen_img_vid_with_refs" / ".venv" / "bin" / "python")


async def generate_image_via_mcp(
    prompt: str,
    face_reference_paths: list[str] = None,
    background_reference_path: str = None,
    pose_reference_path: str = None,
    item_reference_paths: list[str] = None,
) -> str:
    """Call generate_custom_scene_image tool on the MCP server via stdio."""
    server_params = StdioServerParameters(
        command=MCP_VENV_PYTHON,
        args=[MCP_SERVER_PATH],
        env=dict(os.environ),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            arguments = {"prompt": prompt}
            if face_reference_paths:
                arguments["face_reference_paths"] = face_reference_paths
            if background_reference_path:
                arguments["background_reference_path"] = background_reference_path
            if pose_reference_path:
                arguments["pose_reference_path"] = pose_reference_path
            if item_reference_paths:
                arguments["item_reference_paths"] = item_reference_paths

            result = await session.call_tool("generate_custom_scene_image", arguments=arguments)

            if result.content:
                for content in result.content:
                    if hasattr(content, "text"):
                        return content.text

            return "Error: No result returned from MCP server"


async def process_yaml(input_path: Path, output_dir: Path):
    with open(input_path, "r", encoding="utf-8") as f:
        scenes = yaml.safe_load(f)

    if not isinstance(scenes, list):
        print("Error: YAML content must be a list of scene objects.")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loaded {len(scenes)} scenes from {input_path}")
    print(f"Output directory: {output_dir}")
    print()

    mapping = []

    for idx, scene in enumerate(scenes):
        scene_num = idx + 1
        prompt = scene.get("prompt", "")
        face_refs = scene.get("face_reference_paths") or []
        bg_ref = scene.get("background_reference_path")
        pose_ref = scene.get("pose_reference_path")
        item_refs = scene.get("item_reference_paths") or []

        face_refs = [p for p in face_refs if p is not None]
        item_refs = [p for p in item_refs if p is not None]

        print(f"[{scene_num}/{len(scenes)}] Generating image via MCP...")
        print(f"  Prompt: {prompt[:120]}{'...' if len(prompt) > 120 else ''}")

        result = await generate_image_via_mcp(
            prompt=prompt,
            face_reference_paths=face_refs if face_refs else None,
            background_reference_path=bg_ref,
            pose_reference_path=pose_ref,
            item_reference_paths=item_refs if item_refs else None,
        )

        if result.startswith("Error"):
            print(f"  FAILED: {result}")
            mapping.append({
                "scene": scene_num,
                "filename": None,
                "prompt": prompt,
                "error": result,
            })
        else:
            src = Path(result)
            ext = src.suffix or ".png"
            dest_filename = f"scene_{scene_num:02d}{ext}"
            dest_path = output_dir / dest_filename
            shutil.copy2(src, dest_path)

            print(f"  OK -> {dest_filename}")
            mapping.append({
                "scene": scene_num,
                "filename": dest_filename,
                "prompt": prompt,
            })

    mapping_path = output_dir / "mapping.yaml"
    with open(mapping_path, "w", encoding="utf-8") as f:
        yaml.dump(mapping, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print()
    print(f"Done. {len(mapping)} images processed.")
    print(f"Mapping saved to: {mapping_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images from a scene YAML file via MCP protocol."
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        required=True,
        help="Path to the input YAML file (e.g. outputs/scene_10_images_office_01.yaml)",
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=None,
        help="Base output directory. Defaults to the same directory as the input YAML file.",
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: Input YAML file not found: {input_path}")
        sys.exit(1)

    folder_name = input_path.stem
    if args.output_dir:
        base_dir = Path(args.output_dir)
    else:
        base_dir = input_path.parent

    output_dir = base_dir / folder_name

    asyncio.run(process_yaml(input_path, output_dir))


if __name__ == "__main__":
    main()
