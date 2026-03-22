import streamlit as st
import os
import json
import subprocess
from pathlib import Path
import time
from datetime import datetime

# Configuration
st.set_page_config(layout="wide", page_title="MCP Media Generator", page_icon="🎨")

# Paths
BASE_DIR = Path(__file__).parent.absolute()
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

MCP_DIR = Path("/home/dd/work/diep/openhands/apps/mcp_gen_img_vid_with_refs")
MCP_PYTHON = MCP_DIR / ".venv" / "bin" / "python"
MCP_OUTPUTS_DIR = MCP_DIR / "outputs"

# Helper functions
def save_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None
    file_path = UPLOADS_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(file_path.absolute())

def run_mcp_tool(tool_name, kwargs):
    # Create a temporary script to run the tool
    script_path = BASE_DIR / "run_tool.py"
    script_content = f"""
import sys
import json
sys.path.append('{MCP_DIR}')
from server import {tool_name}

kwargs = {json.dumps(kwargs)}
try:
    result = {tool_name}(**kwargs)
    print(json.dumps({{"status": "success", "result": result}}))
except Exception as e:
    print(json.dumps({{"status": "error", "message": str(e)}}))
"""
    with open(script_path, "w") as f:
        f.write(script_content)
    
    try:
        # Run the script using the MCP virtual environment python
        env = os.environ.copy()
        env["PYTHONPATH"] = str(MCP_DIR)
        
        process = subprocess.run(
            [str(MCP_PYTHON), str(script_path)],
            capture_output=True,
            text=True,
            env=env,
            cwd=str(MCP_DIR), # Run in MCP dir so outputs go to MCP_DIR/outputs
            timeout=300 # 5 minutes timeout
        )
        
        if process.returncode != 0:
            return {"status": "error", "message": f"Process failed with code {process.returncode}\\nStderr: {process.stderr}"}
            
        try:
            # Find the last line that is valid JSON
            lines = process.stdout.strip().split('\\n')
            for line in reversed(lines):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
            return {"status": "error", "message": f"Could not parse output as JSON. Stdout: {process.stdout}"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to parse output: {str(e)}\\nStdout: {process.stdout}"}
            
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "MCP tool execution timed out after 5 minutes."}
    except Exception as e:
        return {"status": "error", "message": f"Execution failed: {str(e)}"}
    finally:
        if script_path.exists():
            script_path.unlink()

def get_output_files():
    if not MCP_OUTPUTS_DIR.exists():
        return []
    
    files = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.mp4"]:
        files.extend(MCP_OUTPUTS_DIR.glob(ext))
        
    # Sort by modification time, newest first
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return files

# UI Layout
st.title("🎨 MCP Media Generator")

# Tabs for different tools
tab1, tab2 = st.tabs(["🖼️ Generate Image", "🎬 Generate Video"])

with tab1:
    st.header("Generate Custom Scene Image")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.form("image_gen_form"):
            prompt = st.text_area("Prompt", "A beautiful landscape", help="The description of the new scene/context.")
            
            st.subheader("References (Optional)")
            face_refs = st.file_uploader("Face References", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
            bg_ref = st.file_uploader("Background Reference", type=["png", "jpg", "jpeg"])
            pose_ref = st.file_uploader("Pose Reference", type=["png", "jpg", "jpeg"])
            item_refs = st.file_uploader("Item References", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
            
            submit_img = st.form_submit_button("Generate Image", type="primary")
            
        # Preview uploaded references
        if face_refs or bg_ref or pose_ref or item_refs:
            st.subheader("Reference Previews")
            preview_cols = st.columns(4)
            if bg_ref:
                preview_cols[0].image(bg_ref, caption="Background", use_container_width=True)
            if pose_ref:
                preview_cols[1].image(pose_ref, caption="Pose", use_container_width=True)
            if face_refs:
                for i, f in enumerate(face_refs[:2]): # Preview up to 2 faces
                    preview_cols[2].image(f, caption=f"Face {i+1}", use_container_width=True)
            if item_refs:
                for i, f in enumerate(item_refs[:2]): # Preview up to 2 items
                    preview_cols[3].image(f, caption=f"Item {i+1}", use_container_width=True)
            
        if submit_img:
            with st.spinner("Generating image... This may take a while."):
                # Save files and get absolute paths
                face_paths = [save_uploaded_file(f) for f in face_refs] if face_refs else None
                bg_path = save_uploaded_file(bg_ref) if bg_ref else None
                pose_path = save_uploaded_file(pose_ref) if pose_ref else None
                item_paths = [save_uploaded_file(f) for f in item_refs] if item_refs else None
                
                kwargs = {
                    "prompt": prompt,
                    "face_reference_paths": face_paths,
                    "background_reference_path": bg_path,
                    "pose_reference_path": pose_path,
                    "item_reference_paths": item_paths
                }
                
                # Remove None values
                kwargs = {k: v for k, v in kwargs.items() if v is not None}
                
                result = run_mcp_tool("generate_custom_scene_image", kwargs)
                
                if result.get("status") == "success":
                    output_path = result.get("result")
                    if output_path and output_path.startswith("Error"):
                        st.error(output_path)
                    else:
                        st.session_state.last_generated_image = output_path
                        st.success("Image generated successfully!")
                else:
                    st.error(f"Error: {result.get('message')}")
                    
                with st.expander("Debug Logs"):
                    st.json(result)

    with col2:
        st.subheader("Result Preview")
        if "last_generated_image" in st.session_state and st.session_state.last_generated_image:
            try:
                st.image(st.session_state.last_generated_image, caption="Newly Generated Image", use_container_width=True)
            except Exception as e:
                st.error(f"Could not load image: {e}")
        else:
            st.info("Generated image will appear here.")

with tab2:
    st.header("Generate Video from Scene Image")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.form("video_gen_form"):
            vid_prompt = st.text_area("Prompt", "A cinematic pan of the scene", help="The description of the video.")
            
            context_img = st.file_uploader("Context Image (Required)", type=["png", "jpg", "jpeg"])
            
            orientation = st.selectbox("Orientation", ["horizontal", "vertical"])
            
            submit_vid = st.form_submit_button("Generate Video", type="primary")
            
        if context_img:
            st.subheader("Context Image Preview")
            st.image(context_img, use_container_width=True)
            
        if submit_vid:
            if not context_img:
                st.error("Context Image is required!")
            else:
                with st.spinner("Generating video... This may take several minutes."):
                    img_path = save_uploaded_file(context_img)
                    
                    kwargs = {
                        "prompt": vid_prompt,
                        "image_path": img_path,
                        "orientation": orientation
                    }
                    
                    result = run_mcp_tool("generate_video_from_scene_image", kwargs)
                    
                    if result.get("status") == "success":
                        output_path = result.get("result")
                        if output_path and output_path.startswith("Error"):
                            st.error(output_path)
                        else:
                            st.session_state.last_generated_video = output_path
                            st.success("Video generated successfully!")
                    else:
                        st.error(f"Error: {result.get('message')}")
                        
                    with st.expander("Debug Logs"):
                        st.json(result)

    with col2:
        st.subheader("Result Preview")
        if "last_generated_video" in st.session_state and st.session_state.last_generated_video:
            try:
                st.video(st.session_state.last_generated_video)
            except Exception as e:
                st.error(f"Could not load video: {e}")
        else:
            st.info("Generated video will appear here.")

# Gallery Section
st.divider()
st.header("📁 Output Gallery")

output_files = get_output_files()

if not output_files:
    st.info("No output files found yet.")
else:
    # Create a dictionary mapping display names to file paths
    file_options = {}
    for f in output_files:
        mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        display_name = f"{f.name} ({mtime})"
        file_options[display_name] = f
        
    selected_file_name = st.selectbox(
        "Select a file to preview", 
        options=list(file_options.keys()),
        index=0
    )
    
    if selected_file_name:
        selected_file = file_options[selected_file_name]
        
        st.subheader(f"Preview: {selected_file.name}")
        
        if selected_file.suffix.lower() in ['.mp4']:
            st.video(str(selected_file))
        else:
            st.image(str(selected_file), use_container_width=True)
