# Note: bản fasthtml không ổn lắm, nó generate thiếu input form và có vẻ mount chưa chuẩn.
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runner import run_task

cwd="/home/dd/work/diep/openhands/apps/web_play_mcp_img_vid_fasthtml"
# 2. Nhiệm vụ: Nâng cấp FastHTML (Fix Mount & Multi-upload)
task_prompt = f"""
Ứng dụng fasthtml dùng để gọi mcp sinh ảnh và sinh video ở thư mục này: `{cwd}`
Hiện nay, khi tôi kiểm tra thì phía web nó có hiển thị đầy đủ các thứ tôi mong muốn.
Tuy nhiên lỗi là ở chỗ khi sinh ảnh, tôi thấy các ảnh reference được truyền xuống không đến được mcp. Tôi cho rằng ứng dụng này quản lý đường dẫn chưa tốt. Bạn hãy review rồi đánh giá cho tôi xem có tìm được lỗi ở đâu không?
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
