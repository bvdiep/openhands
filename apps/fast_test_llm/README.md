# FastHTML LLM Tester

Giao diện web phát triển bằng FastHTML để kiểm thử và quản lý lịch sử các câu lệnh gửi tới LLM.

## Tính năng
- Form nhập liệu cho System Prompt, User Query, Model, Temperature, và Max Tokens.
- Hỗ trợ gọi LLM thông qua LiteLLM (OpenAI compatible).
- Hiển thị kết quả ngay lập tức bằng AJAX (HTMX).
- Trạng thái loading khi đang chờ phản hồi từ LLM.
- Lưu trữ lịch sử tất cả các yêu cầu và phản hồi vào cơ sở dữ liệu SQLite.
- Xem danh sách lịch sử có phân trang và xem chi tiết từng lần thực thi.

## Cài đặt

### 1. Chuẩn bị môi trường
Yêu cầu Python 3.9 trở lên.

```bash
# Tạo môi trường ảo (khuyến nghị)
python -m venv venv
source venv/bin/activate  # Trên Linux/MacOS
# hoặc
venv\Scripts\activate     # Trên Windows
```

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường
Tạo file `.env` từ file mẫu `.env.example`:
```bash
cp .env.example .env
```
Chỉnh sửa `.env` và điền `OPENAI_API_KEY` của bạn cũng như cấu hình model mong muốn.

## Khởi chạy
Chạy ứng dụng bằng lệnh:
```bash
python main.py
```
Sau khi chạy, truy cập vào `http://localhost:5001` (hoặc cổng mặc định của FastHTML) để bắt đầu sử dụng.

## Cấu trúc thư mục
- `main.py`: Mã nguồn chính của ứng dụng.
- `llm_history.db`: Cơ sở dữ liệu SQLite (tự động tạo khi chạy).
- `.env`: Cấu hình API key và mặc định.
- `requirements.txt`: Danh sách các thư viện cần thiết.
