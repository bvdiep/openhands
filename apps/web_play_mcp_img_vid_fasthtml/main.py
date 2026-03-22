import os
import sys
import asyncio
import json
import uuid
import re
import time
from pathlib import Path
from dotenv import load_dotenv
from fasthtml.common import *
from starlette.staticfiles import StaticFiles
from starlette.datastructures import UploadFile
from starlette.responses import RedirectResponse

# Load environment variables
load_dotenv()
LOGIN_USER = os.getenv("LOGIN_USER", "admin")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "admin")

# Paths
MCP_DIR = os.path.abspath("/home/dd/work/diep/openhands/apps/mcp_gen_img_vid_with_refs")
OUTPUTS_DIR = os.path.join(MCP_DIR, "outputs")
UPLOADS_DIR = os.path.abspath("/home/dd/work/diep/openhands/apps/web_play_mcp_img_vid_fasthtml/uploads")
VENV_PYTHON = os.path.join(MCP_DIR, ".venv", "bin", "python")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Extract schema
# sys.path.append(MCP_DIR)
# from server import mcp

def get_tools_schema():
    import subprocess
    import json
    import os
    # Use the MCP app's venv to run get_schema.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_script = os.path.join(current_dir, "get_schema.py")
    result = subprocess.run([VENV_PYTHON, schema_script], capture_output=True, text=True, cwd=current_dir)
    try:
        # Find the JSON part in case there are warnings
        output = result.stdout
        start_idx = output.find('{')
        if start_idx != -1:
            return json.loads(output[start_idx:])
        else:
            print(f"Schema stdout: {result.stdout}")
            print(f"Schema stderr: {result.stderr}")
        return {}
    except Exception as e:
        print(f"Error parsing schema: {e}")
        return {}

tools_schema = get_tools_schema()

# Auth check
def before_auth(req, session):
    auth = session.get('auth')
    if not auth and req.scope['path'] not in ['/login', '/logout']:
        return RedirectResponse('/login', status_code=303)

app, rt = fast_app(
    pico=True,
    static_path='static',
    before=before_auth,
    secret_key=os.getenv("SECRET_KEY", "some-very-secret-key-123"),
    hdrs=(
        Style("""
            .scrollable { max-height: 80vh; overflow-y: auto; }
            .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
            .gallery-item img, .gallery-item video { max-width: 100%; height: auto; border-radius: 8px; }
            .preview-area { text-align: center; margin-bottom: 2rem; border: 1px solid #ccc; padding: 1rem; border-radius: 8px; }
            .preview-area img, .preview-area video { max-width: 100%; max-height: 70vh; }
            .error-msg { color: red; }
            footer { font-size: 0.8em; margin-top: 0.5rem; }
            .loader {
                border: 2px solid #f3f3f3;
                border-top: 2px solid #3498db;
                border-radius: 50%;
                width: 12px;
                height: 12px;
                animation: spin 2s linear infinite;
                display: inline-block;
                margin-left: 10px;
                vertical-align: middle;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .htmx-indicator { display: none; }
            .htmx-request .htmx-indicator { display: inline-block; }
            .htmx-request.htmx-indicator { display: inline-block; }
        """),
    )
)

# Use absolute paths for mounting
app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

@rt("/outputs/{path:path}")
async def serve_outputs(path: str):
    return FileResponse(os.path.join(OUTPUTS_DIR, path))

@rt("/uploads/{path:path}")
async def serve_uploads(path: str):
    return FileResponse(os.path.join(UPLOADS_DIR, path))

def render_form(tool_name):
    tool = tools_schema.get(tool_name)
    if not tool:
        return Div("Tool not found")
    
    schema = tool["schema"]
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    
    fields = []
    for prop_name, prop_info in properties.items():
        is_required = prop_name in required
        prop_type = prop_info.get("type")
        title = prop_info.get("title", prop_name)
        
        # Determine input type
        if prop_name == "orientation":
             fields.append(
                Div(
                    Label(title + (" *" if is_required else "")),
                    Select(
                        Option("Horizontal (16:9)", value="horizontal"),
                        Option("Vertical (9:16)", value="vertical"),
                        name=prop_name, required=is_required
                    )
                )
            )
        elif prop_type == "string":
            if "path" in prop_name.lower() or "image" in prop_name.lower():
                fields.append(
                    Div(
                        Label(title + (" *" if is_required else "")),
                        Input(type="file", name=prop_name, required=is_required, accept="image/*,video/*")
                    )
                )
            elif prop_name == "prompt":
                fields.append(
                    Div(
                        Label(title + (" *" if is_required else "")),
                        Textarea(name=prop_name, required=is_required, rows=4)
                    )
                )
            else:
                fields.append(
                    Div(
                        Label(title + (" *" if is_required else "")),
                        Input(type="text", name=prop_name, required=is_required)
                    )
                )
        elif prop_type == "array":
            if "path" in prop_name.lower() or "image" in prop_name.lower():
                max_items = 3
                if "face" in prop_name.lower():
                    max_items = 2
                elif "item" in prop_name.lower():
                    max_items = 4
                
                fields.append(
                    Div(
                        Label(title + (" *" if is_required else "")),
                        Div(
                            *[Input(type="file", name=prop_name, accept="image/*,video/*", style="margin-bottom: 5px;") for _ in range(max_items)],
                        ),
                        P(f"You can upload up to {max_items} reference images for this field.", style="font-size: 0.8em; color: gray;")
                    )
                )
            else:
                fields.append(
                    Div(
                        Label(title + (" *" if is_required else "")),
                        Input(type="text", name=prop_name, required=is_required, placeholder="Comma separated values")
                    )
                )
        elif prop_type == "boolean":
            fields.append(
                Div(
                    Label(
                        Input(type="checkbox", name=prop_name),
                        title
                    )
                )
            )
        elif prop_type == "number" or prop_type == "integer":
            fields.append(
                Div(
                    Label(title + (" *" if is_required else "")),
                    Input(type="number", name=prop_name, required=is_required)
                )
            )
            
    return Form(
        *fields,
        Input(type="hidden", name="tool_name", value=tool_name),
        Button(
            "Execute", 
            Span(cls="loader htmx-indicator"),
            type="submit", id="execute-btn"
        ),
        hx_post="/execute", hx_target="#latest-output", hx_indicator=".htmx-indicator",
        hx_disabled_elt="#execute-btn",
        enctype="multipart/form-data", hx_encoding="multipart/form-data"
    )

def get_gallery_items():
    files = []
    for f in os.listdir(OUTPUTS_DIR):
        path = os.path.join(OUTPUTS_DIR, f)
        if os.path.isfile(path):
            files.append((f, os.path.getmtime(path)))
    files.sort(key=lambda x: x[1], reverse=True)
    
    items = []
    for f, _ in files:
        ext = f.lower().split('.')[-1]
        url = f"/outputs/{f}"
        if ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
            items.append(
                Article(
                    Header(P(f, style="font-size: 0.7em; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;")),
                    Img(src=url, hx_get=f"/view?file={f}", hx_target="#latest-output", style="cursor: pointer;"),
                    Footer(
                        A("View", hx_get=f"/view?file={f}", hx_target="#latest-output", style="margin-right: 10px; cursor: pointer;"),
                        A("Download", href=url, download=f)
                    ),
                    cls="gallery-item"
                )
            )
        elif ext in ['mp4', 'webm']:
            items.append(
                Article(
                    Header(P(f, style="font-size: 0.7em; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;")),
                    Video(src=url, controls=True),
                    Footer(
                        A("View", hx_get=f"/view?file={f}", hx_target="#latest-output", style="margin-right: 10px; cursor: pointer;"),
                        A("Download", href=url, download=f)
                    ),
                    cls="gallery-item"
                )
            )
    return items


@rt("/login")
def get():
    return Titled("MCP Control Center", 
        Main(
            Card(
                Form(
                    Label("Username", Input(type="text", name="username", placeholder="Username")),
                    Label("Password", Input(type="password", name="password", placeholder="Password")),
                    Button("Login", cls="contrast"),
                    method="post"
                ),
                header=Header(H2("Authentication Required"))
            ),
            cls="container", style="max-width: 400px; margin-top: 100px;"
        )
    )

@rt("/login")
def post(username: str, password: str, session):
    if username == LOGIN_USER and password == LOGIN_PASSWORD:
        session['auth'] = username
        return RedirectResponse('/', status_code=303)
    return Titled("MCP Control Center", 
        Main(
            Card(
                P("Invalid username or password", style="color: red;"),
                Form(
                    Label("Username", Input(type="text", name="username", placeholder="Username")),
                    Label("Password", Input(type="password", name="password", placeholder="Password")),
                    Button("Login", cls="contrast"),
                    method="post"
                ),
                header=Header(H2("Authentication Required"))
            ),
            cls="container", style="max-width: 400px; margin-top: 100px;"
        )
    )

@rt("/logout")
def get(session):
    session.pop('auth', None)
    return RedirectResponse('/login', status_code=303)

@rt("/")
def get():
    tool_options = [Option(t, value=t) for t in tools_schema.keys()]
    
    return Titled("Hạ Vy - MCP Control Center",
        Div(A("Logout", href="/logout"), style="text-align: right; margin-bottom: 10px;"),
        Grid(
            # Left Column: Form
            Div(
                Article(
                    H2("Input"),
                    Label("Select Tool"),
                    Select(*tool_options, name="tool_name", hx_get="/form", hx_target="#form-container"),
                    Div(render_form(list(tools_schema.keys())[0]), id="form-container"),
                ),
                cls="scrollable"
            ),
            # Right Column: Preview & Gallery
            Div(
                Article(
                    H2("Latest Output"),
                    Div(id="loading", cls="htmx-indicator", style="display:none;")(
                        "Processing..."
                    ),
                    Div(id="latest-output", cls="preview-area"),
                    H2("Gallery"),
                    Div(*get_gallery_items(), cls="gallery", id="gallery"),
                ),
                cls="scrollable"
            )
        )
    )

@rt("/form")
def get(tool_name: str):
    return render_form(tool_name)

@rt("/view")
def get(file: str):
    ext = file.lower().split('.')[-1]
    url = f"/outputs/{file}"
    if ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
        return Img(src=url)
    elif ext in ['mp4', 'webm']:
        return Video(src=url, controls=True, autoplay=True)
    return Div("Unsupported file type")

async def save_upload(upload: UploadFile) -> str:
    if not upload.filename:
        return ""
    ext = upload.filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(UPLOADS_DIR, filename)
    content = await upload.read()
    with open(path, "wb") as f:
        f.write(content)
    return path

@rt("/execute")
async def post(request):
    form = await request.form()
    tool_name = form.get("tool_name")
    
    if not tool_name or tool_name not in tools_schema:
        return Div(Ins("Invalid tool selected", cls="error-msg"))
        
    tool = tools_schema[tool_name]
    schema = tool["schema"]
    properties = schema.get("properties", {})
    
    kwargs = {}
    for prop_name, prop_info in properties.items():
        prop_type = prop_info.get("type")
        
        if prop_type == "array":
            files = form.getlist(prop_name)
            paths = []
            for f in files:
                if isinstance(f, UploadFile) and f.filename:
                    path = await save_upload(f)
                    if path:
                        paths.append(path)
            if paths:
                kwargs[prop_name] = paths
        elif prop_type == "string" and ("path" in prop_name.lower() or "image" in prop_name.lower()):
            f = form.get(prop_name)
            if isinstance(f, UploadFile) and f.filename:
                path = await save_upload(f)
                if path:
                    kwargs[prop_name] = path
        else:
            val = form.get(prop_name)
            if val:
                if prop_type == "boolean":
                    kwargs[prop_name] = val.lower() in ['true', 'on', '1']
                elif prop_type == "number":
                    kwargs[prop_name] = float(val)
                elif prop_type == "integer":
                    kwargs[prop_name] = int(val)
                else:
                    kwargs[prop_name] = val
                    
    # Execute tool via subprocess
    start_time = time.time()
    print(f"\n[MCP] Executing tool: {tool_name}")
    print(f"[MCP] Arguments: {json.dumps(kwargs, indent=2, default=str)}")
    if "prompt" in kwargs:
        print(f"[MCP] Prompt: {kwargs['prompt']}")

    script_path = os.path.join(UPLOADS_DIR, f"exec_{uuid.uuid4().hex}.py")
    with open(script_path, "w") as f:
        f.write(f"""
import sys
import json
sys.path.append('{MCP_DIR}')
from server import mcp
import asyncio

async def main():
    try:
        kwargs = {repr(kwargs)}
        result = await mcp.call_tool('{tool_name}', kwargs)
        # Handle content list
        serializable_result = []
        if isinstance(result, list):
            for item in result:
                if hasattr(item, 'dict'):
                    serializable_result.append(item.dict())
                elif hasattr(item, 'model_dump'):
                    serializable_result.append(item.model_dump())
                else:
                    # try to extract what we can
                    serializable_result.append(str(item))
        else:
            serializable_result = str(result)
            
        print(json.dumps({{"status": "success", "result": serializable_result}}))
    except Exception as e:
        import traceback
        print(json.dumps({{"status": "error", "error": str(e), "traceback": traceback.format_exc()}}))

asyncio.run(main())
""")

    import subprocess
    try:
        process = subprocess.run([VENV_PYTHON, script_path], capture_output=True, text=True, timeout=300, cwd=MCP_DIR)
        os.remove(script_path)
        
        if process.returncode != 0:
            print(f"[MCP] Subprocess error: {process.stderr}")
            return Div(Ins(f"Subprocess error: {process.stderr}", cls="error-msg"))
            
        try:
            out = json.loads(process.stdout)
            if out.get("status") == "error":
                print(f"[MCP] Tool error: {out.get('error')}")
                return Div(Ins(f"Tool error: {out.get('error')}", cls="error-msg"))
                
            result = out.get("result")
            print(f"[MCP] Success: {result}")
            
            # Let's extract the text from the result
            text_result = ""
            if isinstance(result, list):
                for item in result:
                    if isinstance(item, dict):
                        if item.get("type") == "text":
                            text_result += item.get("text", "")
                    else:
                        text_result += str(item)
            else:
                text_result = str(result)
            
            # Try to find a path in the result
            found_path = None
            
            # 1. Check if the text itself is a path
            potential_path = text_result.strip()
            if potential_path.startswith("Result: "):
                potential_path = potential_path[len("Result: "):].strip()
            # remove surrounding quotes if any
            potential_path = potential_path.strip("'\"")
            
            if os.path.exists(potential_path):
                found_path = potential_path
            else:
                # 2. Look for path-like strings in text_result
                # Can be absolute or relative to MCP_DIR
                matches = re.findall(r'([^\s\'"]+\.(?:png|jpg|jpeg|gif|webp|mp4|webm))', text_result)
                for m in matches:
                    p = m if os.path.isabs(m) else os.path.join(MCP_DIR, m)
                    if os.path.exists(p):
                        found_path = p
                        break
            
            # 3. If still not found, check OUTPUTS_DIR for newest file created after start_time
            if not found_path:
                new_files = []
                for f in os.listdir(OUTPUTS_DIR):
                    p = os.path.join(OUTPUTS_DIR, f)
                    if os.path.isfile(p) and os.path.getmtime(p) > start_time:
                        new_files.append((p, os.path.getmtime(p)))
                if new_files:
                    new_files.sort(key=lambda x: x[1], reverse=True)
                    found_path = new_files[0][0]
            
            gallery_update = Div(*get_gallery_items(), cls="gallery", id="gallery", hx_swap_oob="true")
            
            if found_path and os.path.exists(found_path):
                filename = os.path.basename(found_path)
                ext = filename.lower().split('.')[-1]
                
                # Determine URL based on where the file is
                if OUTPUTS_DIR in found_path:
                    url = f"/outputs/{filename}"
                elif UPLOADS_DIR in found_path:
                    url = f"/uploads/{filename}"
                else:
                    url = f"/outputs/{filename}" 
                
                if ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                    return Div(Img(src=url), gallery_update)
                elif ext in ['mp4', 'webm']:
                    return Div(Video(src=url, controls=True, autoplay=True), gallery_update)
            
            # Only show result text if no file path found
            return Div(P(f"Result: {text_result}"), gallery_update)
            
        except json.JSONDecodeError:
            return Div(Ins(f"Invalid JSON output: {process.stdout}", cls="error-msg"))
            
    except subprocess.TimeoutExpired:
        os.remove(script_path)
        return Div(Ins("Execution timed out", cls="error-msg"))
    except Exception as e:
        return Div(Ins(f"Execution failed: {str(e)}", cls="error-msg"))

serve()
