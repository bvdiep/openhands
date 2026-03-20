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
mcp = FastMCP("ImageGeneratorWithFaceRef")

@mcp.tool()
def generate_image_with_refs(
    prompt: str, 
    face_reference_paths: list[str] = None,
    background_reference_path: str = None,
    pose_reference_path: str = None,
    item_reference_path: str = None
) -> str:
    """
    Generate an image using Google's Gemini model with various optional reference images.
    
    Args:
        prompt: The description of the new scene/context.
        face_reference_paths: Optional list of paths to reference images containing faces.
        background_reference_path: Optional path to a reference image for the background/scene.
        pose_reference_path: Optional path to a reference image for the character's pose.
        item_reference_path: Optional path to a reference image for a specific item to include.
        
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
        if item_reference_path and not os.path.exists(item_reference_path):
            return f"Error: Item reference image not found at {item_reference_path}"
            
        # Ensure outputs directory exists
        output_dir = Path("./outputs")
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

        # 3. Item
        if item_reference_path and os.path.exists(item_reference_path):
            instruction_parts.append("\n- Include this specific item in the image exactly as shown:")
            contents.extend(["\nItem Reference:", Image.open(item_reference_path)])

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

if __name__ == "__main__":
    mcp.run()
