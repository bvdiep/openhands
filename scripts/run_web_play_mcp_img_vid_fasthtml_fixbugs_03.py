# Note: bản fasthtml không ổn lắm, nó generate thiếu input form và có vẻ mount chưa chuẩn.
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runner import run_task

cwd="/home/dd/work/diep/openhands/apps/web_play_mcp_img_vid_fasthtml"
# 2. Nhiệm vụ: Nâng cấp FastHTML (Fix Mount & Multi-upload)
task_prompt = f"""
Ứng dụng fasthtml dùng để gọi mcp sinh ảnh và sinh video ở thư mục này: `{cwd}`
Tôi muốn tối ưu thêm một chút trải nghiệm người dùng như sau:
1. Bổ sung hiển thị log kỹ hơn vào console khi tôi chạy pm2 (ví dụ prompt tổng hợp hay các thông tin có giá trị khác)
2. Cho phép nhập tối đa 2 faces thôi. Hiện nay bạn cho nhập 3.
3. Cho phép nhập tối đa 4 items. Hiện nay đang tối đa là 3.
4. Khi thực hiện bằng nút Execute, nút đã disable nhưng tôi muốn thêm hiệu ứng loading (một icon nhỏ nhỏ đang xoay chẳng hạn) để thể hiện việc đang thực hiện.
5. Ở chỗ Latest Output, thay vì hiển thị output của mcp khi thực hiện xong thì hãy hiển thị luôn ảnh kết quả trên đó. Chỉ hiển thị output của mcp nếu có lỗi.
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
