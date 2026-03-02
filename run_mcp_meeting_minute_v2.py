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
cwd = os.path.join(os.getcwd(), "mcp_meeting_minutes_v2")
if not os.path.exists(cwd):
    os.makedirs(cwd)

conversation = Conversation(agent=agent, workspace=cwd)

# 4. Prompt xây dựng MCP Server
task_prompt = """
Hãy xây dựng một MCP Server bằng Python trong thư mục hiện tại để xử lý âm thanh cuộc họp bằng Gemini Multimodal Live API theo các tiêu chuẩn sau:

1. THIẾT LẬP MÔI TRƯỜNG:
   - Tạo venv tên '.venv'. Mọi lệnh python/pip PHẢI dùng từ '.venv' này.
   - Cài đặt: mcp, python-dotenv, google-genai, pydub.
   - Yêu cầu cài đặt 'ffmpeg' trên hệ thống (ghi vào README).

2. LOGIC MCP SERVER (server.py):
   - Tool: 'transcribe_meeting_native'.
   - Input: 'file_path' (Đường dẫn tuyệt đối đến file âm thanh local).
   - Pipeline xử lý (Sử dụng Multimodal Live API):
     a. Khởi tạo kết nối: Dùng 'google.genai.Client' với 'live.connect' để tận dụng endpoint Native Audio (hạn mức 1M TPM).
     b. Streaming: Đọc file audio qua 'pydub', chuyển đổi về định dạng PCM 16-bit 16kHz (hoặc định dạng tối ưu cho Gemini Live).
     c. Gửi dữ liệu: Stream các khối audio nhỏ (chunks) qua kết nối Websocket của Live API.
     d. Nhận phản hồi: Thu thập transcript và thông tin phân vai người nói (Speaker Diarization) trả về từ luồng Live.
   - Trả về: JSON chứa 'full_transcript' với độ chính xác cao cho tiếng Việt và tên người nói (nếu nhận diện được).
   - Cấu hình: Đọc 'GEMINI_API_KEY' từ file .env.

3. ƯU TIÊU TIẾNG VIỆT & NGỮ CẢNH:
   - Cấu hình System Instruction cho model: "Bạn là một chuyên gia gỡ băng tiếng Việt. Hãy nhận diện chính xác các từ lóng, thuật ngữ kỹ thuật và phân biệt các người nói dựa trên sắc thái giọng nói."

4. KIỂM TRA & TÀI LIỆU:
   - Viết requirements.txt.
   - Viết README.md hướng dẫn cấu hình API Key và tích hợp vào Claude Desktop/Telegram Bot.
   - Chạy 'python server.py' để kiểm tra lỗi khởi tạo.
"""

print(f"🚀 OpenHands SDK V1 đang khởi chạy tại: {cwd}")

# 5. Chạy nhiệm vụ
try:
    conversation.send_message(task_prompt)
    # Trong SDK V1, dùng .run() để Agent thực hiện chuỗi hành động cho đến khi xong
    conversation.run() 
    print("\n✅ Nhiệm vụ hoàn tất! Kiểm tra thư mục mcp_meeting_minutes V2.")
except Exception as e:
    print(f"❌ Lỗi thực thi: {e}")