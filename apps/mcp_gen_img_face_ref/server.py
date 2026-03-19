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
def generate_image_with_face(prompt: str, face_reference_path: str = "./hv01.png") -> str:
    """
    Generate an image using Google's Gemini model with a face reference image.
    
    Args:
        prompt: The description of the new scene/context.
        face_reference_path: Path to the reference image containing the face.
        
    Returns:
        The path to the generated image.
    """
    try:
        # Check if reference image exists
        if not os.path.exists(face_reference_path):
            return f"Error: Reference image not found at {face_reference_path}"
            
        # Ensure outputs directory exists
        output_dir = Path("./outputs")
        output_dir.mkdir(exist_ok=True)
        
        # Initialize Google GenAI client
        client = genai.Client()
        
        # Open reference image
        img = Image.open(face_reference_path)
        
        # Call the model
        # The prompt should instruct the model to keep the face from the reference image
        full_prompt = f"Keep the face exactly the same as the reference image. {prompt}"
        
        result = client.models.generate_content(
            model='gemini-3.1-flash-image-preview',
            contents=[img, full_prompt],
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
