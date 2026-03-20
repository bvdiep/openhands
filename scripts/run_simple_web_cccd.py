import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runner import run_task

# 1. Cấu hình
cwd = os.path.join(os.getcwd(), "..", "apps", "simple_web_cccd")

# 2. Nhiệm vụ
task_prompt = f"""
**Mục tiêu:** Xây dựng ứng dụng Flask quản lý CCCD tại {cwd}.

**Yêu cầu kỹ thuật:**
1. **Môi trường:** Thực hiện tại {cwd}. Cài đặt `flask`, `python-dotenv`. 
2. **Bảo mật:** Xác thực qua `ADMIN_USERNAME`/`ADMIN_PASSWORD` trong `.env`. Cần có `SECRET_KEY` cho session.
3. **Database (SQLite):** Bảng `citizens` (id, fullname, id_number, dob, address, issue_date, issue_place, photo_1, photo_2, status='OK').
4. **Xử lý File:**
   - Lưu ảnh vào `static/uploads/`. 
   - Rename file bằng UUID/Timestamp để tránh trùng.
   - Chỉ cho phép upload định dạng: png, jpg, jpeg.

**Các chức năng:**
1. **Login (`/login`):** Form đăng nhập đơn giản, bảo mật.
2. **Dashboard (`/`):** Liệt kê danh sách CCCD dưới dạng Table Bootstrap. Hiển thị thumbnail ảnh, click vào để xem ảnh lớn (modal).
3. **Thêm mới (`/upload`):**
   - Form nhập đầy đủ thông tin + 2 input file cho ảnh.
   - Sau khi lưu thành công, redirect về trang chủ kèm thông báo (flash message).

**Nhiệm vụ cho OpenHands:**
- Khởi tạo project structure.
- Tạo file `.env.example` mẫu.
- Viết `app.py` xử lý logic tập trung, sử dụng Flask-Login hoặc Session để chặn các route nếu chưa đăng nhập.
- Sử dụng Bootstrap 5 (CDN) để giao diện hiện đại.
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
