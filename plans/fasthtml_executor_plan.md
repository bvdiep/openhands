# FastHTML Executor App Plan

## 1. Overview
The FastHTML Executor is a web application built using FastHTML. It allows users to input a prompt and specify a model to execute a backend process. The application provides real-time streaming of execution logs (similar to a terminal) and maintains a history of all executions in a SQLite database.

**Location:** `scripts/fasthtml_task_runner/`

## 2. Directory Structure
```text
scripts/fasthtml_task_runner/
├── main.py                 # Core FastHTML application, routes, DB logic, and SSE streaming
├── requirements.txt        # Python dependencies (python-fasthtml, sqlite-minutils, etc.)
├── .gitignore              # Files to ignore in version control (e.g., .db, __pycache__)
├── README.md               # Project documentation and setup instructions
└── ecosystem.config.json   # PM2 configuration for process management
```

## 3. Database Schema
We will use SQLite to store execution history. A local file (e.g., `executor.db`) will be used.

**Table:** `executions`
- `id` (Integer, Primary Key, Auto-increment): Unique identifier for the execution.
- `prompt` (Text): The prompt entered by the user.
- `model` (Text): The model name specified by the user.
- `status` (Text): Current status of the execution. Values: `running`, `success`, `error`.
- `created_at` (Datetime): Timestamp when the execution was initiated.

## 4. UI Flow
1. **Home Page (`/`):**
   - Displays a form with:
     - `prompt`: A `<textarea>` for the user's input.
     - `model`: A `<input type="text">` for the model name (explicitly not a select dropdown).
     - **Execute Button**: Submits the form via HTMX.
   - Below the form, there's a designated "Terminal" section (a `<div>` or `<pre>`) to display logs.
   - A "History" section showing previous executions loaded from the SQLite DB.

2. **Execution Trigger:**
   - When the user clicks "Execute", an HTMX request is sent to the backend.
   - The backend creates a new record in the `executions` table with status `running`.
   - The UI updates the Terminal section to connect to an SSE (Server-Sent Events) or WebSocket endpoint specific to this execution ID.

## 5. Log Streaming (SSE/WebSocket)
1. **Endpoint (e.g., `/stream/{execution_id}`):**
   - The client connects to this endpoint using HTMX SSE extension (`hx-ext="sse"`).
   - The backend process starts executing (simulated or actual subprocess).
   - As the process generates output, the backend yields HTML fragments (e.g., `<div>log line</div>`) to the client.
2. **Completion:**
   - Once the process finishes, the backend yields a final log message: `<div class="success">Thành công</div>` or `<div class="error">Lỗi</div>`.
   - The DB record for `execution_id` is updated to `success` or `error`.
   - The SSE connection is closed by sending a specific termination event.

## 6. Development Steps
1. **Setup:** Create the directory structure and initialize files.
2. **Database:** Setup FastHTML's MiniDataAPI or plain SQLite to define the `executions` table.
3. **UI Layout:** Build the main form and layout components using FastHTML tags.
4. **Execution Logic:** Implement the route to handle form submission, DB insertion, and returning the SSE connection trigger.
5. **Streaming Route:** Implement the SSE generator that mimics process execution, streams logs, and updates DB status upon completion.
6. **Deployment:** Configure `ecosystem.config.json` for running the app via PM2.
