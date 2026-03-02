import os
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.terminal import TerminalTool
from openhands.tools.file_editor import FileEditorTool

# 1. Khởi tạo LLM qua LiteLLM Proxy
llm = LLM(
    model="openai/sonnet-4", 
    base_url="http://localhost:4000/v1", 
    api_key=os.getenv("LITELLM_KEY", "master-diep1234321"),
    temperature=0.0,
)

# 2. Định nghĩa Agent với các công cụ cần thiết
# SDK V1 sử dụng danh sách Tool trực tiếp
agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
    ],
)

# 3. Tạo cuộc hội thoại (Conversation)
# Tham số workspace trỏ đến thư mục dự án của bạn
cwd = os.path.join(os.getcwd(), "mcp_meeting_minutes")
if not os.path.exists(cwd):
    os.makedirs(cwd)

conversation = Conversation(agent=agent, workspace=cwd)

# 4. Prompt xây dựng MCP Server
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

print(f"🚀 OpenHands SDK V1 đang khởi chạy tại: {cwd}")

# 5. Chạy nhiệm vụ
try:
    conversation.send_message(task_prompt)
    # Trong SDK V1, dùng .run() để Agent thực hiện chuỗi hành động cho đến khi xong
    conversation.run() 
    print("\n✅ Nhiệm vụ hoàn tất! Kiểm tra thư mục mcp_meeting_minutes.")
except Exception as e:
    print(f"❌ Lỗi thực thi: {e}")