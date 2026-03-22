# Note: bản fasthtml không ổn lắm, nó generate thiếu input form và có vẻ mount chưa chuẩn.
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runner import run_task

# 1. Cấu hình
cwd = os.path.join(os.getcwd(), "..", "apps", "web_play_mcp_img_vid_fasthtml")
cwd_mcp = os.path.join(os.getcwd(), "..", "apps", "mcp_gen_img_vid_with_refs")

# 2. Nhiệm vụ: Nâng cấp FastHTML (Fix Mount & Multi-upload)
task_prompt = f"""
# Role: Senior Python Fullstack Developer (HTMX & FastHTML Expert)
# Context: 
Ứng dụng fastHTML ở thư mục {cwd} đã được triển khai để cho phép chạy mcp (ở {cwd_mcp}) từ trình duyệt. Hiện nay ứng dụng đã được chạy ở cổng 8100 và quản lý bởi pm2 (với index = 1)
Tuy nhiên, vấn đề là khi sử dụng http://localhost:8100 thì trước mắt có hai lỗi như sau:
1. Các ảnh trong Gallery đêù bị lỗi 404.
2. Form để thao tác với mcp sinh ảnh (generate_custom_scene_image) chưa đúng ở hai điểm: thiếu số lượng input files referene và có một số file reference cần upload dạng list.

Hãy kiểm tra code của ứng dụng, kiểm tra cả render trên trình duyệt để tìm lỗi và sửa.
"""

# 3. Chạy nhiệm vụ
if __name__ == "__main__":
    run_task(
        task_prompt=task_prompt,
        workspace=cwd,
      #   model="gemini/gemini-3.1-pro-preview",
        model="gemini/gemini-3-flash-preview",
        api_key=os.getenv("GEMINI_API_KEY", "no-gemini-api-key"),  # Fails fast if not set
        base_url=None,
        success_message="Nhiệm vụ hoàn tất! Kiểm tra code"
    )
