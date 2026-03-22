import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runner import run_task

# 1. Cấu hình
cwd = os.path.join(os.getcwd(), "..", "apps", "web_play_mcp_img_vid")
cwd_mcp = os.path.join(os.getcwd(), "..", "apps", "mcp_gen_img_vid_with_refs")

# 2. Nhiệm vụ
task_prompt = f"""
# Role: Senior Python Developer & AI Architect
# Context: 
Tôi đang phát triển một hệ thống sinh media (Image/Video) dựa trên Model Context Protocol (MCP). 
Hệ thống này sử dụng các file reference (faces, background, accessories) lưu trữ trực tiếp trên SSD của server Ubuntu.

# Task:
Hãy xây dựng một giao diện Web bằng Streamlit để điều khiển các MCP tools này. Thư mục của dự án UI là: `{cwd}`.

# Technical Requirements:
1. **Analysis Phase**: 
   - Truy cập vào thư mục code MCP tại: `{cwd_mcp}`.
   - Hãy phân tích các file định nghĩa công cụ (thường là server.py hoặc các file tools) để hiểu chính xác JSON Schema của các tham số đầu vào và kiểu dữ liệu đầu ra.

2. **File & Storage Management**:
   - Sử dụng `st.file_uploader` để nhận file từ trình duyệt.
   - Lưu file vào: `{cwd}/uploads/`. 
   - Quan trọng: Phải chuyển đổi `relative path` thành `absolute path` trước khi truyền vào MCP để tránh lỗi File Not Found.

3. **Execution Logic**:
   - Sử dụng đường dẫn Python executable từ virtual environment có sẵn tại: `{cwd_mcp}/.venv/bin/python`.
   - Khi thực thi MCP tool qua `subprocess`, hãy đảm bảo sử dụng đường dẫn Python này để tránh lỗi thiếu thư viện.
   - Mỗi tool của MCP phải được trình bày trong một Form riêng biệt (hoặc Tabs).
   - **Giao diện kết quả:** Ngoài việc hiển thị kết quả "Vừa sinh ra" ở cột bên phải, hãy thêm một `st.selectbox` hoặc Gallery ở phía dưới để liệt kê toàn bộ các file đã có trong `{cwd_mcp}/outputs`. Hãy sắp xếp danh sách file ở phần này theo thứ tự thời gian mới nhất lên đầu (Sort by ctime/mtime) để tôi dễ tìm. 
   - Cho phép tôi chọn một file cũ trong danh sách đó để xem lại (Preview) mà không cần chạy lại MCP.

4. **UX/UI Guidelines**:
   - Sử dụng `st.set_page_config(layout="wide")`.
   - Hiển thị song song (Columns): Bên trái là Input/Reference Preview - Bên phải là Result Preview.
   - Thêm phần `st.expander` để hiển thị logs/debug của MCP tool.

5. **Output Artifacts**:
   - File `app.py` và `requirements.txt`.
   - File `.gitignore` (loại bỏ thư mục `uploads/` và `__pycache__`).
   - File `README.md` hướng dẫn setup và chạy `streamlit run app.py --server.headless true`.

# Constraints:
- Xử lý ngoại lệ chặt chẽ: Nếu file không hợp lệ hoặc MCP timeout phải báo lỗi rõ ràng trên UI.
- Code style: Tuân thủ PEP8, sạch sẽ và có comment giải thích các bước quan trọng.
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
