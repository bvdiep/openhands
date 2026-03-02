import os
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.terminal import TerminalTool
from openhands.tools.file_editor import FileEditorTool

# 1. Khởi tạo LLM qua LiteLLM Proxy
llm = LLM(
    model="openai/sonnet-4", 
    base_url="http://localhost:4000/v1", 
    api_key=os.getenv("LITELLM_KEY", "master-diep1234321"),
    temperature=0.0,
)

# 2. Định nghĩa Agent với các công cụ cần thiết
# SDK V1 sử dụng danh sách Tool trực tiếp
agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
    ],
)

# 3. Tạo cuộc hội thoại (Conversation)
# Tham số workspace trỏ đến thư mục dự án của bạn
cwd = os.path.join(os.getcwd(), "mcp_internet")
if not os.path.exists(cwd):
    os.makedirs(cwd)

conversation = Conversation(agent=agent, workspace=cwd)

# 4. Prompt xây dựng MCP Server
task_prompt = """
Hãy xây dựng một MCP Server bằng Python trong thư mục hiện tại theo các tiêu chuẩn sau:

1. THIẾT LẬP MÔI TRƯỜNG:
   - Tạo venv tên '.venv'. Mọi lệnh python/pip PHẢI dùng từ '.venv' này.
   - Cài đặt: mcp, python-dotenv, httpx, trafilatura, voyageai.

2. LOGIC MCP SERVER (server.py):
   - Tool: 'internet_search'.
   - Pipeline: Serper (Search) -> VoyageAI (rerank-2.5) -> httpx (Crawl) -> Trafilatura (Clean).
   - Loại bỏ link Youtube, Facebook, Instagram.
   - Set User-Agent cho crawler và timeout 10s.
   - Đọc API Key từ file .env có sẵn.

3. KIỂM TRA:
   - Viết requirements.txt và README.md hướng dẫn cấu hình vào Claude Desktop.
   - Chạy thử 'python server.py' để check lỗi cú pháp.
"""

print(f"🚀 OpenHands SDK V1 đang khởi chạy tại: {cwd}")

# 5. Chạy nhiệm vụ
try:
    conversation.send_message(task_prompt)
    # Trong SDK V1, dùng .run() để Agent thực hiện chuỗi hành động cho đến khi xong
    conversation.run() 
    print("\n✅ Nhiệm vụ hoàn tất! Kiểm tra thư mục mcp_internet.")
except Exception as e:
    print(f"❌ Lỗi thực thi: {e}")