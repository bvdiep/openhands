import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runner import run_task

cwd="/home/dd/work/diep/openhands/scripts/fasthtml_task_runner"
# 2. Nhiệm vụ: Nâng cấp FastHTML (Fix Mount & Multi-upload)
task_prompt = f"""
Ứng dụng fasthtml dùng để gọi openhands thực thi nhiệm vụ code ở thư mục này: `{cwd}`
Tôi muốn tối ưu trải nghiệm thêm như sau:
1. Nút nhấn Execute hiện nay vẫn enabled sau khi click, dẫn đến việc có thể bị click nhiều lần. Hãy disable nó đi và cho một icon nho nhỏ thể hiện việc đang hoạt động.
2. Log tôi đã thấy thẻ hiện rât tốt ở pm2 log, nhưng trên giao diện tôi thấy nó chỉ hiện lên toàn bộ khi đã hoàn thành. Liệu có thể thể hiện realtime tương tự như ở log pm2 được không?
3. Tôi cũng muốn lưu cả log tổng thể vào database. Hãy bổ sung thêm cột cho việc này.
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
