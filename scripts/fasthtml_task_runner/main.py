import os
import sqlite3
import asyncio
import json
import sys
import threading
from datetime import datetime
from fasthtml.common import *
from starlette.responses import StreamingResponse

# Add the root directory to sys.path so we can import the engine module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Add the virtual environment's site-packages to sys.path to import openhands
venv_path = "/home/dd/python/envs/openhands"
if os.path.exists(venv_path):
    site_packages = os.path.join(venv_path, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages")
    if os.path.exists(site_packages):
        sys.path.insert(0, site_packages)

# Database setup
DB_FILE = "executor.db"

def init_db():
    """Initialize the SQLite database with executions table"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            model TEXT NOT NULL,
            workspace TEXT NOT NULL,
            status TEXT NOT NULL,
            logs TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Check if logs column exists, if not add it
    c.execute("PRAGMA table_info(executions)")
    columns = [column[1] for column in c.fetchall()]
    if 'logs' not in columns:
        c.execute("ALTER TABLE executions ADD COLUMN logs TEXT")
    conn.commit()
    conn.close()

def add_execution(prompt, model, workspace):
    """Add a new execution record and return its ID"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO executions (prompt, model, workspace, status) VALUES (?, ?, ?, ?)",
        (prompt, model, workspace, "running")
    )
    exec_id = c.lastrowid
    conn.commit()
    conn.close()
    return exec_id

def update_execution_status(exec_id, status, logs=None):
    """Update the status and logs of an execution"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if logs is not None:
        c.execute(
            "UPDATE executions SET status = ?, logs = ? WHERE id = ?",
            (status, logs, exec_id)
        )
    else:
        c.execute(
            "UPDATE executions SET status = ? WHERE id = ?",
            (status, exec_id)
        )
    conn.commit()
    conn.close()

def get_executions(page=1, page_size=10):
    """Get executions from the database with pagination"""
    offset = (page - 1) * page_size
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Sort by ID descending as requested
    c.execute(
        "SELECT id, prompt, model, workspace, status, logs, created_at FROM executions ORDER BY id DESC LIMIT ? OFFSET ?",
        (page_size, offset)
    )
    rows = c.fetchall()
    
    # Get total count for pagination
    c.execute("SELECT COUNT(*) FROM executions")
    total_count = c.fetchone()[0]
    
    conn.close()
    return [
        {
            "id": row[0],
            "prompt": row[1],
            "model": row[2],
            "workspace": row[3],
            "status": row[4],
            "logs": row[5],
            "created_at": row[6]
        }
        for row in rows
    ], total_count

def get_execution(exec_id):
    """Get a single execution by ID from the database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT id, prompt, model, workspace, status, logs, created_at FROM executions WHERE id = ?",
        (exec_id,)
    )
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "prompt": row[1],
            "model": row[2],
            "workspace": row[3],
            "status": row[4],
            "logs": row[5],
            "created_at": row[6]
        }
    return None

def render_history(page=1):
    page_size = 10
    executions, total_count = get_executions(page, page_size)
    total_pages = (total_count + page_size - 1) // page_size
    
    pagination_controls = []
    if total_pages > 1:
        # Prev button
        if page > 1:
            pagination_controls.append(Button("Prev", hx_get=f"/history?page={page-1}", hx_target="#history-container", cls="outline small"))
        
        # Page info
        pagination_controls.append(Span(f"Page {page} of {total_pages}"))
        
        # Next button
        if page < total_pages:
            pagination_controls.append(Button("Next", hx_get=f"/history?page={page+1}", hx_target="#history-container", cls="outline small"))

    return Div(
        H3("Execution History"),
        Table(
            Thead(
                Tr(
                    Th("ID"),
                    Th("Prompt"),
                    Th("Model"),
                    Th("Workspace"),
                    Th("Status"),
                    Th("Created At")
                )
            ),
            Tbody(
                *[Tr(
                    Td(A(str(exec["id"]), hx_get=f"/execution/{exec['id']}", hx_target="#modal-placeholder")),
                    Td(exec["prompt"][:50] + ("..." if len(exec["prompt"]) > 50 else "")),
                    Td(exec["model"]),
                    Td(exec["workspace"]),
                    Td(exec["status"], cls=f"status-{exec['status']}"),
                    Td(exec["created_at"])
                ) for exec in executions]
            ) if executions else Tr(Td("No executions yet", colspan=6)),
            cls="history-table"
        ),
        Div(*pagination_controls, cls="pagination-container")
    )



# Initialize database on startup
init_db()

# Global dictionary to store queues for each execution
execution_queues = {}

class QueueWriter:
    """Helper class to redirect stdout to an asyncio queue and collect logs"""
    def __init__(self, queue, loop):
        self.queue = queue
        self.loop = loop
        self.full_logs = []

    def write(self, data):
        if data:
            self.full_logs.append(data)
            # Put the data into the asyncio queue
            asyncio.run_coroutine_threadsafe(self.queue.put(data), self.loop)
            # Also write to the original stdout
            sys.__stdout__.write(data)
            sys.__stdout__.flush()

    def flush(self):
        sys.__stdout__.flush()

    def get_logs(self):
        return "".join(self.full_logs)

    @property
    def encoding(self):
        return getattr(sys.__stdout__, 'encoding', 'utf-8')

# FastHTML app setup
app, rt = fast_app(
    pico=True,
    hdrs=(
        Style("""
            .terminal { 
                border: 1px solid #ccc; 
                padding: 1rem; 
                margin: 1rem 0; 
                min-height: 100px; 
                background-color: #1e1e1e; 
                color: #d4d4d4;
                font-family: 'Courier New', Courier, monospace;
                overflow-y: auto;
                max-height: 500px;
                white-space: pre-wrap;
                border-radius: 4px;
            }
            .history-table { width: 100%; border-collapse: collapse; }
            .history-table th, .history-table td { 
                border: 1px solid #ddd; 
                padding: 0.5rem; 
                text-align: left; 
            }
            .history-table th { background-color: #f2f2f2; }
            .status-running { color: orange; font-weight: bold; }
            .status-success { color: green; font-weight: bold; }
            .status-error { color: red; font-weight: bold; }
            .error { color: red; font-weight: bold; margin-bottom: 1rem; }
            .loading-indicator { display: none; }
            .htmx-request .loading-indicator, .is-loading .loading-indicator { display: flex; align-items: center; justify-content: center; }
            .htmx-request .normal-text, .is-loading .normal-text { display: none; }
            .htmx-request.button-execute, .is-loading.button-execute { pointer-events: none; opacity: 0.8; }
            .spinner {
                display: inline-block;
                width: 1.2rem;
                height: 1.2rem;
                border: 2px solid rgba(255,255,255,.3);
                border-radius: 50%;
                border-top-color: #fff;
                animation: spin 0.8s linear infinite;
                margin-right: 0.5rem;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            #execution-modal article {
                width: 90%;
                max-width: 1200px;
            }
            .pagination-container {
                display: flex;
                align-items: center;
                justify-content: center;
                margin-top: 1rem;
                gap: 1rem;
            }
            .pagination-container button {
                margin-bottom: 0;
            }
        """),
    )
)

@rt("/")
def get():
    """Render the main page with form and history"""
    return Titled("Task Runner",
        Div(
            # Form section
            Form(
                H3("Execute Task"),
                Label("Prompt:", fr="prompt"),
                Textarea(name="prompt", id="prompt", rows=4, required=True),
                Label("Model:", fr="model"),
                Input(type="text", name="model", id="model", required=True, value="gemini/gemini-3-flash-preview"),
                Label("Working Directory:", fr="workspace"),
                Input(type="text", name="workspace", id="workspace", required=True, value="."),
                Button(
                    Div(Span(cls="spinner"), "Execute", cls="loading-indicator"),
                    Span("Execute", cls="normal-text"),
                    type="submit", 
                    hx_post="/execute", 
                    hx_target="#executions-container", 
                    cls="button-execute"
                ),
                id="task-form"
            ),
            
            # Loading indicator
            Div(
                Span("Loading...", cls="loading-indicator"),
                id="loading-indicator"
            ),
            
            # Container for executions
            Div(id="executions-container"),
            
            # Modal placeholder
            Div(id="modal-placeholder"),
            
            # History section
            Div(render_history(1), id="history-container")
        )
    )

@rt("/history")
def get(page: int = 1):
    """Handle pagination for history table"""
    return render_history(page)

@rt("/execute")
async def post(request):
    """Handle form submission and start execution"""
    form = await request.form()
    prompt = form.get("prompt", "").strip()
    model = form.get("model", "").strip()
    workspace = form.get("workspace", "").strip()
    
    if not prompt or not model or not workspace:
        return Div("Prompt, model, and workspace are required", cls="error")
    
    # Create execution record
    exec_id = add_execution(prompt, model, workspace)
    
    # Create a queue for this execution
    loop = asyncio.get_running_loop()
    q = asyncio.Queue()
    execution_queues[exec_id] = q
    
    # Start the task in a background thread
    def run_task_thread():
        # Redirect stdout to our queue writer
        old_stdout = sys.stdout
        writer = QueueWriter(q, loop)
        sys.stdout = writer
        try:
            # Import here to avoid circular imports
            from engine.runner import TaskRunner
            
            runner = TaskRunner(
                workspace=workspace,
                model=model
                # Other parameters can be added from form if needed
            )
            runner.run(prompt, success_message="Nhiệm vụ hoàn tất!")
            # Update status to success with logs
            update_execution_status(exec_id, "success", writer.get_logs())
        except Exception as e:
            # Log the error
            sys.stdout.write(f"Error: {str(e)}\n")
            import traceback
            traceback.print_exc()
            # Update status to error with logs
            update_execution_status(exec_id, "error", writer.get_logs())
        finally:
            # Restore stdout
            sys.stdout = old_stdout
            # Put a sentinel to indicate the end of the stream
            asyncio.run_coroutine_threadsafe(q.put(None), loop)
    
    thread = threading.Thread(target=run_task_thread)
    thread.start()
    
    # Return initial response with the execution container and a script to handle real-time logs
    return Div(
        H4(f"Execution #{exec_id} started"),
        Div(
            id=f"terminal-output-{exec_id}",
            cls="terminal",
        ),
        Script(f"""
            (function() {{
                const term = document.getElementById('terminal-output-{exec_id}');
                const btn = document.querySelector('.button-execute');
                if (btn) {{
                    btn.classList.add('is-loading');
                    btn.disabled = true;
                }}
                const source = new EventSource('/stream/{exec_id}');
                source.onmessage = function(event) {{
                    term.textContent += event.data + '\\n';
                    term.scrollTop = term.scrollHeight;
                }};
                source.onerror = function(event) {{
                    source.close();
                    if (btn) {{
                        btn.classList.remove('is-loading');
                        btn.disabled = false;
                    }}
                }};
            }})();
        """),
        id=f"execution-{exec_id}"
    )

@rt("/stream/{exec_id}")
async def get(exec_id: int):
    """Server-Sent Events endpoint for log streaming"""
    async def event_stream():
        q = execution_queues.get(exec_id)
        if q is None:
            return

        while True:
            try:
                line = await q.get()
            except asyncio.CancelledError:
                break

            if line is None:  # Sentinel indicating end of stream
                # Small delay to ensure all messages are processed
                await asyncio.sleep(0.1)
                break
            
            # SSE format requires "data: " prefix and "\n\n" suffix
            # For multiline data, each line should have "data: " prefix
            lines = line.splitlines(keepends=True)
            for l in lines:
                # remove trailing newline for the data part, SSE adds it
                data_content = l.rstrip('\n').rstrip('\r')
                yield f"data: {data_content}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        }
    )


@rt("/execution/{exec_id}")
def get_execution_detail(exec_id: int):
    """Get the details of a specific execution for the modal"""
    exec_data = get_execution(exec_id)
    if not exec_data:
        return Dialog(
            Article(
                Header(
                    Button(aria_label="Close", cls="close", onclick="this.closest('dialog').removeAttribute('open')", type="button"),
                    P(Strong("Error"))
                ),
                P("Execution not found"),
            ),
            open=True
        )
    
    return Dialog(
        Article(
            Header(
                Button(aria_label="Close", cls="close", onclick="this.closest('dialog').removeAttribute('open')", type="button"),
                P(Strong(f"Execution Details #{exec_id}"))
            ),
            Div(
                P(Strong("ID: "), str(exec_data["id"]), " (ngày ", exec_data["created_at"], ", status ", Span(exec_data["status"], cls=f"status-{exec_data['status']}"), ")"),
                P(Strong("Model: "), exec_data["model"]),
                P(Strong("Workspace: "), exec_data["workspace"]),
                P(Strong("Prompt:")),
                Pre(exec_data["prompt"], style="white-space: pre-wrap; background: #f4f4f4; padding: 10px; border-radius: 4px;"),
                P(Strong("Logs:")),
                Pre(exec_data["logs"] or "No logs available", cls="terminal", style="max-height: 300px; overflow-y: auto;")
            ),
            Footer(
                Button("Close", onclick="this.closest('dialog').removeAttribute('open')", type="button")
            )
        ),
        open=True,
        id="execution-modal"
    )

serve()