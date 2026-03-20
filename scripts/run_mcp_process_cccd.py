import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runner import run_task

# 1. Cấu hình đường dẫn
cwd_web = os.path.join(os.getcwd(), "..", "apps", "simple_web_cccd")
cwd = os.path.join(os.getcwd(), "..", "apps", "mcp_process_cccd")

# 2. Nhiệm vụ cho OpenHands
task_prompt = f"""
**Mục tiêu:** Xây dựng một MCP Server (Python) sử dụng `FastMCP` để thực hiện luồng: OCR ảnh CCCD bằng Gemini 3 Flash -> Tự động điền form bằng Playwright vào ứng dụng Flask tại `{cwd_web}`.

### 1. Cấu hình hệ thống
- **Thư mục triển khai MCP (Workdir):** `{cwd}`
- **Templates tham chiếu (Cần đọc để trích xuất Selector):**
  - Login: `{cwd_web}/templates/login.html`
  - Upload: `{cwd_web}/templates/upload.html`
- **Model AI:** `gemini-3-flash-preview`

### 2. Nhiệm vụ Tiền xử lý (Pre-processing)
- **Phân tích Selector:** Đọc nội dung 2 file template trên. Trích xuất chính xác thuộc tính `id` hoặc `name` của các thẻ `<input>` (fullname, id_number, dob, address, issue_date, issue_place, status, photo_1, photo_2).
- **Yêu cầu:** Playwright phải sử dụng đúng các selector này, không được hard-code.

### 3. Xây dựng các MCP Tools (FastMCP)

#### Tool 1: `extract_cccd_with_gemini`
- **Input:** Đường dẫn 2 ảnh (mặt trước/sau).
- **Logic:** Sử dụng `google-generativeai`.
- **System Prompt:**
  > "Bạn là chuyên gia OCR dữ liệu hành chính Việt Nam. Trích xuất thông tin từ 2 ảnh CCCD thành JSON.
  > **Quy tắc:**
  > - `dob`, `issue_date`: Định dạng `YYYY-MM-DD`.
  > - `id_number`: Chuỗi 12 số.
  > - Nếu mờ/thiếu: Dùng giá trị mặc định `1111-11-11` (date) và `không xác định` (text). Đặt `status` là `WARNING`.
  > - Nếu đầy đủ: Đặt `status` là `OK`.
  > - JSON Output duy nhất: {{"fullname": "...", "id_number": "...", "dob": "...", "address": "...", "issue_date": "...", "issue_place": "...", "status": "..."}}."

#### Tool 2: `automate_web_submission`
- **Input:** JSON data (từ Tool 1) và đường dẫn tuyệt đối của 2 ảnh.
- **Logic Playwright:**
  1. Đăng nhập vào `APP_URL/login` (Lấy URL, User, Pass từ `.env`).
  2. Truy cập `APP_URL/upload`.
  3. Điền toàn bộ thông tin từ JSON.
  4. Upload 2 file ảnh bằng `set_input_files` (Yêu cầu đường dẫn tuyệt đối).
  5. Click Submit và kiểm tra kết quả (flash message hoặc redirect).

#### Tool 3 (Master Tool): `process_and_submit_cccd`
- **Input:** Đường dẫn tuyệt đối của `photo_1` và `photo_2`.
- **Logic:** Gọi tuần tự Tool 1 để lấy dữ liệu, sau đó truyền kết quả trực tiếp vào Tool 2.
- **Output:** Báo cáo tổng kết quá trình (Ví dụ: "Đã trích xuất thành công với trạng thái WARNING và đã upload lên hệ thống").

### 4. Yêu cầu triển khai (Implementation Details)
- **Framework:** `mcp[cli]` với lớp `FastMCP`. Định nghĩa tool bằng `@mcp.tool()`.
- **Khả năng chạy:** Hỗ trợ `python mcp_server.py` và `mcp dev mcp_server.py`.
- **Dependencies:** `requirements.txt` gồm: `mcp[cli]`, `playwright`, `google-generativeai`, `python-dotenv`.
- **Environment:**
  - Tạo `.env` (APP_URL=http://127.0.0.1:5005, ADMIN_USERNAME=admin, ADMIN_PASSWORD=secret, GEMINI_API_KEY=).
  - Tạo `.env.example`.
- **Logging:** Log chi tiết: "Đang phân tích ảnh...", "Đang đăng nhập...", "Đang điền form cho CCCD [ID]...".
- **Playwright:** Chạy async, cài đặt browser bằng `playwright install chromium`.
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
