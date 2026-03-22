# Note: bản fasthtml không ổn lắm, nó generate thiếu input form và có vẻ mount chưa chuẩn.
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runner import run_task

cwd="/home/dd/work/diep/openhands/apps/web_play_mcp_img_vid_fasthtml"
# 2. Nhiệm vụ: Nâng cấp FastHTML (Fix Mount & Multi-upload)
task_prompt = f"""
Ứng dụng fasthtml dùng để gọi mcp sinh ảnh và sinh video ở thư mục này: `{cwd}`
Tôi muốn tối ưu ứng dụng này ở mấy việc sau:
1. Form nhập Prompt hiện nay là dạng input. Hãy sửa thành Text area
2. Hiện nay khi nhấn nút Execute, tôi thấy nó không disable nút, dẫn đến có thể nhấn nhiều lần. Cần có cơ chế disable khi vừa thực hiện.
3. Khi thực hiện xong, tôi thấy nó hiển thị một text output lên ô "Latest Output". Tôi muốn nó enable lại nút Execute (vừa nói ở trên) đồng thời thể hiện danh sách ảnh output được cập nhật)
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
