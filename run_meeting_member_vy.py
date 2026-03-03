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
cwd = os.path.join(os.getcwd(), "meeting_member_vy")
if not os.path.exists(cwd):
    os.makedirs(cwd)

conversation = Conversation(agent=agent, workspace=cwd)

# 4. Prompt xây dựng ứng dụng thành viên cuộc họp (không dùng MCP)
task_prompt = """
Hãy xây dựng một ứng dụng Python trực tiếp trong thư mục hiện tại để tạo thành viên cuộc họp thời gian thực sử dụng Gemini Flash 2.5 Native Audio (Multimodal Live API) theo các tiêu chuẩn sau:

1. THIẾT LẬP MÔI TRƯỜNG:
   - Tạo venv tên '.venv'. Mọi lệnh python/pip PHẢI dùng từ '.venv' này.
   - Cài đặt: python-dotenv, google-genai, pydub, pyaudio, websocket-client.
   - Yêu cầu cài đặt 'ffmpeg' trên hệ thống (ghi vào README).

2. ỨNGDỤNG CHÍNH (app.py hoặc main.py):
   - Sử dụng google.genai.Client với live.connect() để kết nối Gemini Flash 2.5 Native Audio.
   - Xử lý audio thời gian thực:
     a. Thu âm từ microphone hoặc đọc từ file audio.
     b. Chuyển đổi về định dạng PCM 16-bit 16kHz qua pydub.
     c. Stream audio chunks qua WebSocket tới Gemini Live API.
   - Phát hiện tên: Theo dõi transcript để phát hiện khi "Hạ Vy" hoặc "Vy" được nhắc đến.
   - Phản hồi: Chỉ HIỂN THỊ TEXT trên terminal khi tên thành viên được đề cập. KHÔNG phát audio qua loa.
   - Trả về: JSON chứa 'response' (phản hồi của Vy) và 'follow_up_actions' (nếu có).
   - Cấu hình: Đọc 'GEMINI_API_KEY' từ file .env.

3. HỆ THỐNG LOG (LOGGING):
   - Cấu hình log level qua biến môi trường 'LOG_LEVEL' hoặc file config.
   - LOG_LEVEL='production': Chỉ hiển thị khi Vy được gọi và phản hồi của Vy.
   - LOG_LEVEL='debug': Hiển thị toàn bộ transcript, audio chunks, connection status, timing.
   - Mặc định: LOG_LEVEL='info' - hiển thị thời gian, người nói, nội dung chính.
   - Sử dụng Python logging module với các level: DEBUG, INFO, WARNING, ERROR.

4. GIAO DIỆN TERMINAL:
   - Hiển thị rõ ràng khi Vy được gọi: "🔔 [Hạ Vy được gọi]"
   - Hiển thị phản hồi của Vy với định dạng đẹp: "💬 Vy: [phản hồi]"
   - Hiển thị timestamp cho mỗi sự kiện quan trọng.

5. HƯỚNG DẪN HỆ THỐNG (System Instruction):
   - Định nghĩa Vy là "Hạ Vy" - một thành viên cuộc họp chuyên nghiệp.
   - Vy lắng nghe cuộc họp trong thời gian thực.
   - Vy CHỈ phản hồi khi được gọi tên "Hạ Vy" hoặc "Vy".
   - Vy cần phản hồi ngắn gọn, lịch sự và liên quan đến nội dung cuộc họp.
   - Nếu không được gọi, Vy tiếp tục lắng nghe (không phản hồi).

6. YÊU CẦU KỸ THUẬT:
   - Sử dụng google.genai.Client với model='gemini-2.0-flash-exp' hoặc phiên bản Flash 2.5 mới nhất.
   - Cấu hình MultimodalLiveConfig cho audio input (chỉ input, không cần output).
   - Xử lý audio với pydub: AudioSegment.from_file() -> set_frame_rate(16000) -> set_sample_width(2) -> raw_data.
   - Sử dụng pyaudio chỉ để thu âm từ microphone (input), KHÔNG phát audio ra loa.
   - Theo dõi buffer âm thanh và phát hiện từ khóa trong transcript.
   - Config logging: sử dụng biến môi trường LOG_LEVEL (production/info/debug).

7. KIỂM TRA & TÀI LIỆU:
   - Viết requirements.txt.
   - Viết README.md hướng dẫn cấu hình API Key, LOG_LEVEL, chạy ứng dụng.
   - Chạy 'python main.py' để kiểm tra lỗi khởi tạo.
"""

print(f"🚀 OpenHands SDK V1 đang khởi chạy tại: {cwd}")

# 5. Chạy nhiệm vụ
try:
    conversation.send_message(task_prompt)
    # Trong SDK V1, dùng .run() để Agent thực hiện chuỗi hành động cho đến khi xong
    conversation.run() 
    print("\n✅ Nhiệm vụ hoàn tất! Kiểm tra thư mục meeting_member_vy.")
except Exception as e:
    print(f"❌ Lỗi thực thi: {e}")
