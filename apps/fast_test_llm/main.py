import os
from datetime import datetime
from dotenv import load_dotenv
from fasthtml.common import *
from litellm import completion

# Load environment variables
load_dotenv()

# Database setup
db_path = 'llm_history.db'
db = database(db_path)
executions = db.t.executions
if executions not in db.t:
    executions.create(
        id=int, 
        system_prompt=str, 
        user_query=str, 
        model=str, 
        temperature=float, 
        max_tokens=int, 
        response=str, 
        timestamp=str,
        pk='id'
    )
Execution = executions.dataclass()

# App setup
hdrs = (
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
    Style("""
        :root { --pico-font-size: 1rem; }
        main.container { padding-top: 1rem; }
        h1 { font-size: 1.5rem; }
        h3 { font-size: 1.2rem; }
        pre { white-space: pre-wrap; padding: 1rem; border-radius: 8px; background-color: var(--pico-code-background-color); }
        .loading-spinner { border: 2px solid #f3f3f3; border-top: 2px solid #3498db; border-radius: 50%; width: 16px; height: 16px; animation: spin 2s linear infinite; display: inline-block; margin-right: 8px; vertical-align: middle; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        #loading { display: none; }
        .htmx-request#loading { display: inline-block; }
        .htmx-request #loading { display: inline-block; }
    """)
)
app, rt = fast_app(hdrs=hdrs)

def get_llm_response(system_prompt, user_query, model, temp, max_tokens):
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        response = completion(
            model=model,
            messages=messages,
            temperature=float(temp),
            max_tokens=int(max_tokens)
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def ExecutionRow(e):
    return Tr(
        Td(A(e.id, href=f"/detail/{e.id}")),
        Td(e.model),
        Td(e.user_query[:50] + "..." if len(e.user_query) > 50 else e.user_query),
        Td(e.timestamp)
    )

def ExecutionTable(page=1, per_page=10):
    offset = (page - 1) * per_page
    total = len(executions())
    rows = executions(limit=per_page, offset=offset, order_by='id DESC')
    
    table = Table(
        Thead(Tr(Th("ID"), Th("Model"), Th("Query"), Th("Timestamp"))),
        Tbody(*[ExecutionRow(r) for r in rows])
    )
    
    prev_link = A("Previous", hx_get=f"/history?page={page-1}", hx_target="#history-section") if page > 1 else "Previous"
    next_link = A("Next", hx_get=f"/history?page={page+1}", hx_target="#history-section") if offset + per_page < total else "Next"

    pagination = Nav(
        Ul(
            Li(prev_link),
            Li(f"Page {page}"),
            Li(next_link)
        ),
        aria_label="Pagination"
    )
    
    return Div(H3("Execution History"), table, pagination, id="history-section")

@rt("/")
def get(page: int = 1):
    form = Form(method="post", hx_post="/", hx_target="#result", hx_indicator="#loading", hx_disabled_elt="#submit-btn")(
        Grid(
            Div(Label("Model", Input(name="model", value=os.getenv("MODEL", "gpt-3.5-turbo"), required=True))),
            Div(Label("Temperature", Input(name="temperature", type="number", step="0.1", value=os.getenv("TEMPERATURE", "0.7"), required=True))),
            Div(Label("Max Tokens", Input(name="max_tokens", type="number", value=os.getenv("MAX_TOKENS", "1000"), required=True))),
        ),
        Label("System Prompt", Textarea(name="system_prompt", rows=3, placeholder="You are a helpful assistant.", required=True)),
        Label("User Query", Textarea(name="user_query", rows=5, placeholder="Enter your query here...", required=True)),
        Button(Span(cls="loading-spinner", id="loading"), "Submit", type="submit", id="submit-btn"),
    )
    
    return Title("LLM Tester"), Main(cls="container")(
        H1("LLM Tester Interface"),
        form,
        Hr(),
        Div(id="result"),
        Hr(),
        ExecutionTable(page=page)
    )

@rt("/")
def post(system_prompt: str, user_query: str, model: str, temperature: float, max_tokens: int):
    # Call LLM
    response_text = get_llm_response(system_prompt, user_query, model, temperature, max_tokens)
    
    # Save to DB
    new_exec = executions.insert(
        system_prompt=system_prompt,
        user_query=user_query,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        response=response_text,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    # Return result and trigger history update
    return Div(
        H3("Result:"),
        Pre(response_text),
        hx_trigger="load", hx_get="/history", hx_target="#history-section"
    )

@rt("/history")
def get_history(page: int = 1):
    return ExecutionTable(page=page)

@rt("/detail/{id}")
def get_detail(id: int):
    try:
        e = executions.get(id)
        return Title(f"Execution Detail {id}"), Main(cls="container")(
            H1(f"Execution Detail - ID: {id}"),
            A("Back to Home", href="/"),
            Card(
                H4("Configuration"),
                P(B("Model: "), e.model),
                P(B("Temperature: "), e.temperature),
                P(B("Max Tokens: "), e.max_tokens),
                P(B("Timestamp: "), e.timestamp),
                H4("System Prompt"),
                Pre(e.system_prompt),
                H4("User Query"),
                Pre(e.user_query),
                H4("Response"),
                Pre(e.response)
            )
        )
    except Exception:
        return P("Execution not found.")

serve()
