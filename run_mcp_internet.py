import os
from openhands_operation.runner import run_task

# 1. Cấu hình
cwd = os.path.join(os.getcwd(), "mcp_internet")

# 2. Nhiệm vụ
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

# 3. Chạy nhiệm vụ
if __name__ == "__main__":
    run_task(
        task_prompt=task_prompt,
        workspace=cwd,
        model="openai/sonnet-4",
        success_message="Nhiệm vụ hoàn tất! Kiểm tra thư mục mcp_internet."
    )
