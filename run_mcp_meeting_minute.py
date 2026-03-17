import os
from openhands_v2.runner import run_task

# 1. Cấu hình
cwd = os.path.join(os.getcwd(), "mcp_meeting_minutes")

# 2. Nhiệm vụ
task_prompt = """
Hãy xây dựng một MCP Server bằng Python trong thư mục hiện tại để xử lý âm thanh cuộc họp theo các tiêu chuẩn sau:

1. THIẾT LẬP MÔI TRƯỜNG:
   - Tạo venv tên '.venv'. Mọi lệnh python/pip PHẢI dùng từ '.venv' này.
   - Cài đặt: mcp, python-dotenv, groq, pydub, librosa.
   - Đảm bảo hệ thống có 'ffmpeg' (viết hướng dẫn cài đặt vào README nếu cần).

2. LOGIC MCP SERVER (server.py):
   - Tool: 'transcribe_meeting'.
   - Input: 'file_path' (Đường dẫn tuyệt đối đến file âm thanh trên local).
   - Pipeline xử lý:
     a. Pre-process: Tự động phát hiện định dạng (hỗ trợ .ogg, .mp3, .wav, .m4a).
     b. Smart Chunking: Nếu file > 25MB, dùng 'pydub' cắt thành các đoạn nhỏ (mỗi đoạn 10 phút) để tránh giới hạn của Groq API.
     c. Transcription: Gửi từng đoạn lên Groq API (Model: whisper-large-v3).
     d. Stitching: Ghép các đoạn văn bản lại theo đúng thứ tự thời gian.
   - Trả về: Một JSON object chứa toàn bộ nội dung văn bản (full_transcript) và tổng thời lượng (duration_seconds).
   - Cấu hình: Đọc 'GROQ_API_KEY' từ file .env.

3. XỬ LÝ LỖI & HIỆU SUẤT:
   - Xử lý ngoại lệ khi file không tồn tại hoặc lỗi API (Rate Limit).
   - Sử dụng cơ chế async của MCP SDK để không làm treo server khi xử lý file lớn.
   - Tự động dọn dẹp (delete) các file audio chunk tạm thời sau khi xử lý xong.

4. KIỂM TRA & TÀI LIỆU:
   - Viết requirements.txt.
   - Viết README.md hướng dẫn cách cấu hình file .env và cách tích hợp vào Claude Desktop hoặc Telegram Bot backend.
   - Chạy lệnh 'python server.py' trong '.venv' để kiểm tra lỗi cú pháp khởi tạo.
"""

# 3. Chạy nhiệm vụ
if __name__ == "__main__":
    run_task(
        task_prompt=task_prompt,
        workspace=cwd,
        model="openai/sonnet-4",
        success_message="Nhiệm vụ hoàn tất! Kiểm tra thư mục mcp_meeting_minutes."
    )
