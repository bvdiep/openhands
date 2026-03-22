import os
import uuid
from pathlib import Path
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from google import genai
from PIL import Image

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("ImageVideoGeneratorWithReference")

@mcp.tool()
def generate_custom_scene_image(
    prompt: str, 
    face_reference_paths: list[str] = None,
    background_reference_path: str = None,
    pose_reference_path: str = None,
    item_reference_paths: list[str] = None
) -> str:
    """
    Generate an image using Google's Gemini model with various optional reference images.
    
    Args:
        prompt: The description of the new scene/context.
        face_reference_paths: Optional list of paths to reference images containing faces.
        background_reference_path: Optional path to a reference image for the background/scene.
        pose_reference_path: Optional path to a reference image for the character's pose.
        item_reference_paths: Optional list of paths to reference images for specific items to include.
        
    Returns:
        The path to the generated image.
    """
    try:
        # Validate paths
        if face_reference_paths:
            for path in face_reference_paths:
                if not os.path.exists(path):
                    return f"Error: Face reference image not found at {path}"
        if background_reference_path and not os.path.exists(background_reference_path):
            return f"Error: Background reference image not found at {background_reference_path}"
        if pose_reference_path and not os.path.exists(pose_reference_path):
            return f"Error: Pose reference image not found at {pose_reference_path}"
        if item_reference_paths:
            for path in item_reference_paths:
                if not os.path.exists(path):
                    return f"Error: Item reference image not found at {path}"
            
        # Ensure outputs directory exists
        output_dir = Path(__file__).parent / "outputs"
        output_dir.mkdir(exist_ok=True)
        
        # Initialize Google GenAI client
        client = genai.Client()
        
        # Construct the Multi-Modal Payload
        contents = []
        instruction_parts = [prompt, "\n\nStrictly adhere to the following image references:"]

        # 1. Background
        if background_reference_path and os.path.exists(background_reference_path):
            instruction_parts.append("\n- Use this image as the exact scene and background:")
            contents.extend(["\nBackground Reference:", Image.open(background_reference_path)])

        # 2. Pose
        if pose_reference_path and os.path.exists(pose_reference_path):
            instruction_parts.append("\n- The main character must exactly match the body pose in this image:")
            contents.extend(["\nPose Reference:", Image.open(pose_reference_path)])

        # 3. Items
        if item_reference_paths:
            instruction_parts.append(f"\n- Include these {len(item_reference_paths)} specific items exactly as shown:")
            for idx, item_path in enumerate(item_reference_paths):
                if os.path.exists(item_path):
                    contents.extend([f"\nItem Reference {idx + 1}:", Image.open(item_path)])

        # 4. Multiple Faces
        if face_reference_paths:
            instruction_parts.append(f"\n- Keep the faces exactly the same as the {len(face_reference_paths)} provided face references:")
            for idx, face_path in enumerate(face_reference_paths):
                if os.path.exists(face_path):
                    contents.extend([f"\nFace Reference {idx + 1}:", Image.open(face_path)])

        # Combine textual instructions and append at the end
        full_prompt = "".join(instruction_parts)
        contents.append(full_prompt)
        
        result = client.models.generate_content(
            model='gemini-3.1-flash-image-preview',
            contents=contents,
        )
        
        # Extract and save the generated image
        output_filename = f"generated_{uuid.uuid4().hex[:8]}.png"
        output_path = output_dir / output_filename
        
        image_saved = False
        if result.candidates and len(result.candidates) > 0:
            for part in result.candidates[0].content.parts:
                if part.inline_data:
                    with open(output_path, 'wb') as f:
                        f.write(part.inline_data.data)
                    image_saved = True
                    break
                    
        if image_saved:
            return str(output_path.absolute())
        else:
            return "Error: API did not return an image."
            
    except Exception as e:
        return f"Error generating image: {str(e)}"


@mcp.tool()
def generate_video_from_scene_image(
    prompt: str,
    image_path: str,
    orientation: str = "horizontal"
) -> str:
    """
    Generate a video using Google's Veo 3 model from a context image and a description.

    Args:
        prompt: The description of the video.
        image_path: Path to the context image.
        orientation: Video orientation, either "horizontal" (16:9) or "vertical" (9:16).

    Returns:
        The path to the generated video.
    """
    try:
        import time
        from google.genai import types

        if not os.path.exists(image_path):
            return f"Error: Image not found at {image_path}"

        # Ensure outputs directory exists
        output_dir = Path(__file__).parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        # Initialize Google GenAI client
        client = genai.Client()

        # Determine aspect ratio based on orientation
        aspect_ratio = "9:16" if orientation.lower() == "vertical" else "16:9"

        # Start video generation operation
        operation = client.models.generate_videos(
            model='veo-3.1-generate-preview', #'veo-3.0-generate-001', #veo-3.1-generate-preview
            # model="veo-3.1-fast-generate-preview",
            prompt=prompt,
            image=types.Image.from_file(location=image_path),
            config=types.GenerateVideosConfig(
                aspect_ratio=aspect_ratio
            )
        )

        # Poll for completion
        while not operation.done:
            time.sleep(10)
            operation = client.operations.get(operation=operation)

        if operation.error:
            return f"Error generating video: {operation.error}"

        if operation.response and operation.response.generated_videos:
            video = operation.response.generated_videos[0].video
            output_filename = f"generated_video_{uuid.uuid4().hex[:8]}.mp4"
            output_path = output_dir / output_filename

            if video.uri:
                # Download the video using the client
                video_bytes = client.files.download(file=video)
                with open(output_path, 'wb') as f:
                    f.write(video_bytes)
                return str(output_path.absolute())
            elif video.video_bytes:
                with open(output_path, 'wb') as f:
                    f.write(video.video_bytes)
                return str(output_path.absolute())

        return "Error: API did not return a video."

    except Exception as e:
        return f"Error generating video: {str(e)}"

if __name__ == "__main__":
    mcp.run()
