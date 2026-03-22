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
Tôi đang triển khai giao diện điều khiển MCP bằng FastHTML. Thư mục UI: `{cwd}`, Thư mục MCP gốc: `{cwd_mcp}`.

# Task:
Xây dựng Web App FastHTML để quản lý/thực thi MCP tools, khắc phục các lỗi về hiển thị file và thiếu input.

# Technical Requirements:
1. **Deep Analysis & Dynamic Form**:
   - Quét file MCP tại `{cwd_mcp}`: Trích xuất **tất cả** tham số (required & optional) từ JSON Schema.
   - Với các tham số dạng file/image, sử dụng `Input(type="file", multiple=True)` nếu tham số đó chấp nhận danh sách file (ví dụ: reference faces).
   - Đảm bảo mỗi tham số trong Schema đều có một widget tương ứng trên UI (Slider cho số, Input cho text, Checkbox cho boolean).

2. **Static Files & SSD Mounting (CRITICAL)**:
   - Sử dụng `starlette.staticfiles.StaticFiles` để Mount các thư mục ngoài vào FastHTML.
   - Cụ thể: 
     - `/outputs` trỏ đến đường dẫn tuyệt đối: `{cwd_mcp}/outputs`
     - `/uploads` trỏ đến đường dẫn tuyệt đối: `{cwd}/uploads`
   - Đảm bảo code sử dụng `os.path.abspath` để tránh lỗi 404 khi chạy qua PM2.

3. **Backend Logic (HTMX Architecture)**:
   - Dùng `.venv` tại `{cwd_mcp}/.venv/bin/python` để thực thi subprocess.
   - **Xử lý Multi-upload**: Khi nhận `list[UploadFile]`, hãy lưu tất cả vào `{cwd}/uploads/` và truyền danh sách **đường dẫn tuyệt đối** vào MCP tool.
   - Sử dụng `hx-post` để render kết quả "Latest Output" vào cột phải mà không reload trang.

4. **UI Components (Pico CSS)**:
   - Layout: `Grid` 2 cột. Cột trái là Form (scrollable nếu quá dài), cột phải là Preview.
   - **Gallery Section**: Quét folder `{cwd_mcp}/outputs`, hiển thị file theo thứ tự mới nhất. Nút "Xem" sẽ dùng `hx-get` để đưa file đó vào vùng Preview chính.

5. **Output Artifacts**:
   - `main.py`: Chứa logic Mount và Route.
   - `requirements.txt`: Phải có `fasthtml`, `python-multipart`, `uvicorn`.
   - `ecosystem.config.json`: Cấu hình PM2 chạy uvicorn trên port 8100.
   - `README.md` & `.gitignore`.

# Constraints:
- Tuyệt đối không để sót tham số từ MCP Schema.
- Xử lý lỗi: Nếu subprocess trả về lỗi, hiển thị nội dung lỗi vào vùng `Latest Output` với style màu đỏ (Pico CSS: `ins` hoặc `mark`).
"""

# 3. Chạy nhiệm vụ
if __name__ == "__main__":
    run_task(
        task_prompt=task_prompt,
        workspace=cwd,
        model="gemini/gemini-3.1-pro-preview",
        api_key=os.getenv("GEMINI_API_KEY", "no-gemini-api-key"),  # Fails fast if not set
        base_url=None,
        success_message="Nhiệm vụ hoàn tất! Kiểm tra code"
    )
