import os
import asyncio
import logging
import json
import pyaudio
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
from pynput import keyboard

# Load API Key từ file .env
load_dotenv()

# Cấu hình âm thanh chuẩn cho Gemini Live API
FORMAT = pyaudio.paInt16
CHANNELS = 1
INPUT_RATE = 16000  # Input từ microphone
OUTPUT_RATE = 24000  # Output từ Gemini (24kHz)
CHUNK = 1024

# Cấu hình lưu trữ trung gian
AUTO_SAVE_INTERVAL = 60  # Lưu mỗi 60 giây
TEMP_DIR = "temp_recordings"  # Thư mục lưu file tạm

class MeetingMemberVy:
    def __init__(self):
        self.setup_logging()
        self.client = None
        self.session = None  # Lưu session để dùng khi nhấn phím tắt
        self.is_listening = False
        self.transcript_buffer = []
        self.transcript_start_time = None
        self.log_level = "INFO"  # DEBUG, INFO, WARNING, ERROR
        
        # Buffer cho audio tạm
        self.audio_buffer = []
        self.audio_buffer_size = 0
        self.max_buffer_size = 16000 * 60 * 5  # Max 5 phút audio = ~4.8MB
        
        # Tạo thư mục lưu file tạm
        os.makedirs(TEMP_DIR, exist_ok=True)

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        self.logger = logging.getLogger("HaVy")

    def get_system_instruction(self) -> str:
        return """
Bạn là Hà Vy, một trợ lý cuộc họp thông minh.

NHIỆM VỤ:
1. Theo dõi nội dung cuộc họp qua âm thanh.
2. CHỈ phản hồi bằng văn bản khi nghe thấy tên "Hà Vy" hoặc "Vy".
3. Nếu không được gọi tên, hãy im lặng và ghi nhận nội dung.
4. Trả lời ngắn gọn, lịch sự, dùng tiếng Việt tự nhiên.
5. Nếu được hỏi về nội dung trước đó, hãy dựa vào phần transcription bạn đã nghe được.
6. KHI PHẢI TRẢ LỜI: Chỉ trả lời bằng văn bản, không cần phát âm thanh.

HƯỚNG DẪN THÊM:
- Lắng nghe cẩn thận tất cả các cuộc thảo luận trong cuộc họp.
- Khi được gọi, phản hồi ngắn gọn và hữu ích.
- Không ngắt lời hoặc can thiệp khi người khác đang nói.
- Ghi nhớ các quyết định, action items và ngày họp quan trọng.
"""

    def _add_to_transcript_buffer(self, text: str):
        if not self.transcript_start_time:
            self.transcript_start_time = datetime.now()
        
        elapsed = (datetime.now() - self.transcript_start_time).total_seconds()
        timestamp = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d}"
        
        self.logger.info(f"🎤 [{timestamp}] {text}")
        self.transcript_buffer.append({"timestamp": timestamp, "text": text})

    def _add_to_audio_buffer(self, data: bytes):
        """Thêm audio data vào buffer"""
        self.audio_buffer.append(data)
        self.audio_buffer_size += len(data)
        
        # Nếu buffer quá lớn, tự động lưu và reset
        if self.audio_buffer_size >= self.max_buffer_size:
            self._save_audio_buffer()

    async def receive_responses(self, session):
        """Nhận và xử lý phản hồi từ Gemini (cả transcript và text trả lời)"""
        self.session = session
        
        try:
            async for message in session.receive():
                # 1. Xử lý Transcript (SDK mới trả về ở message.transcription)
                if hasattr(message, 'transcription') and message.transcription:
                    text = message.transcription.text.strip()
                    if text:
                        self._add_to_transcript_buffer(text)
                        continue # Nếu là transcript thì bỏ qua các bước sau

                if not message.server_content:
                    continue
                
                if message.server_content.interrupted:
                    self.logger.warning("⚠️ Phiên bị ngắt")
                    continue
                
                # 2. Xử lý model_turn (Câu trả lời của Vy)
                if message.server_content.model_turn:
                    for part in message.server_content.model_turn.parts:
                        if hasattr(part, 'text') and part.text:
                            text = part.text.strip()
                            print(f"\n💬 [VY PHẢN HỒI]: {text}\n")
                            self.logger.info(f"💬 VY phản hồi: {text}")

                # 3. Xử lý Audio (Đúng cấu trúc SDK)
                # Thay vì check message.server_content.audio, ta check trong model_turn
                # Hoặc đơn giản là bỏ qua nếu bạn không cần phát audio ra loa.

        except Exception as e:
            self.logger.error(f"Lỗi nhận dữ liệu chi tiết: {e}")

    async def request_final_minutes(self):
        """Hàm gửi yêu cầu chốt biên bản cuối buổi"""
        if self.session:
            self.logger.info("📝 Đang yêu cầu Hạ Vy lập biên bản cuối buổi...")
            prompt = """
            Cuộc họp đã kết thúc. Dựa trên TOÀN BỘ nội dung âm thanh và ngữ cảnh từ đầu phiên đến giờ, 
            hãy lập một bản BIÊN BẢN CUỘC HỌP chi tiết bao gồm:
            1. Danh sách các người nói (phân biệt bằng âm sắc giọng nói).
            2. Tóm tắt các nội dung thảo luận chính của từng người.
            3. Các quyết định đã chốt và danh sách Action Items (ai làm việc gì, khi nào xong).
            Hãy trình bày thật chuyên nghiệp bằng tiếng Việt.
            """
            # Gửi yêu cầu bằng Text qua luồng Live
            await self.session.send(input=prompt, end_of_turn=True)
            
            # Lưu biên bản ra file
            self.save_final_minutes()
        else:
            self.logger.warning("⚠️ Chưa có session để gửi yêu cầu biên bản")
    
    def save_final_minutes(self):
        """Lưu biên bản cuối buổi ra file"""
        if not self.transcript_buffer: 
            self.logger.warning("⚠️ Không có transcript để lưu biên bản")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"bien_ban_cuoi_buoi_{timestamp}.txt"
        
        # Tạo nội dung biên bản
        content = "=" * 60 + "\n"
        content += "BIÊN BẢN CUỘC HỌP CUỐI BUỔI\n"
        content += f"Thời gian lưu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += "=" * 60 + "\n\n"
        
        content += "--- DANH SÁCH NGƯỜI NÓI ---\n"
        content += "(Phân biệt bằng âm sắc giọng nói trong transcript)\n\n"
        
        content += "--- NỘI DUNG THẢO LUẬN ---\n"
        for item in self.transcript_buffer:
            content += f"[{item['timestamp']}] {item['text']}\n"
        
        content += "\n" + "=" * 60 + "\n"
        content += "(Nội dung trên được lưu tự động. Vui lòng chờ Hà Vy phản hồi chi tiết)\n"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"\n✅ Đã lưu biên bản cuối buổi vào file: {filename}\n")
            self.logger.info(f"💾 Đã lưu biên bản: {filename}")
        except Exception as e:
            self.logger.error(f"Lỗi lưu biên bản: {e}")

    def on_press(self, key):
        """Xử lý khi nhấn phím tắt"""
        try:
            # Nếu nhấn phím 'm' (cho Minutes)
            if key.char == 'm':
                self.logger.info("⌨️ Phát hiện nhấn phím 'm' - Yêu cầu biên bản cuối buổi")
                asyncio.run_coroutine_threadsafe(self.request_final_minutes(), asyncio.get_event_loop())
        except AttributeError:
            pass

    def start_keyboard_listener(self):
        """Khởi động listener cho bàn phím trong thread riêng"""
        listener = keyboard.Listener(on_press=self.on_press)
        listener.daemon = True
        listener.start()
        self.logger.info("⌨️ Keyboard listener đã khởi động (Nhấn 'm' để yêu cầu biên bản)")

    def _save_audio_buffer(self):
        """Lưu buffer audio ra file tạm"""
        if not self.audio_buffer: return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(TEMP_DIR, f"audio_temp_{timestamp}.pcm")
        
        try:
            with open(filename, "wb") as f:
                for chunk in self.audio_buffer:
                    f.write(chunk)
            
            self.logger.info(f"💾 Đã lưu audio tạm: {filename} ({len(self.audio_buffer)} chunks)")
            
            # Reset buffer sau khi lưu
            self.audio_buffer = []
            self.audio_buffer_size = 0
        except Exception as e:
            self.logger.error(f"Lỗi lưu audio tạm: {e}")

    def _save_transcript_temp(self):
        """Lưu transcript tạm thời"""
        if not self.transcript_buffer: return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(TEMP_DIR, f"transcript_temp_{timestamp}.txt")
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"--- TRANSCRIPT TẠM (lưu lúc {timestamp}) ---\n")
                for item in self.transcript_buffer:
                    f.write(f"[{item['timestamp']}] {item['text']}\n")
            
            self.logger.info(f"💾 Đã lưu transcript tạm: {filename}")
        except Exception as e:
            self.logger.error(f"Lỗi lưu transcript tạm: {e}")

    async def send_microphone_audio(self, session):
        """Gửi âm thanh từ microphone lên Gemini Live API"""
        self.logger.info("🔴 Hà Vy đang lắng nghe... (Microphone)")
        p = pyaudio.PyAudio()
        
        # Mở stream với 16kHz cho input
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=INPUT_RATE, 
                        input=True, frames_per_buffer=CHUNK)
        
        self.logger.info("🎤 Microphone đã sẵn sàng (16kHz)")
        
        # Timer cho việc lưu trung gian
        last_save_time = datetime.now()
        
        try:
            while self.is_listening:
                # Đọc dữ liệu từ micro
                data = stream.read(CHUNK, exception_on_overflow=False)
                
                # Lưu vào buffer để backup
                self._add_to_audio_buffer(data)
                
                # Kiểm tra đến lúc lưu định kỳ
                if (datetime.now() - last_save_time).total_seconds() >= AUTO_SAVE_INTERVAL:
                    self._save_audio_buffer()
                    self._save_transcript_temp()
                    last_save_time = datetime.now()
                    self.logger.info(f"🔄 Đã lưu dữ liệu trung gian (audio + transcript)")
                
                # Gửi audio đúng cú pháp: send_realtime_input(audio={...})
                # Sử dụng dict với "data" và "mime_type"
                await session.send_realtime_input(
                    audio={"data": data, "mime_type": "audio/pcm"}
                )
                
                await asyncio.sleep(0.01)
        except Exception as e:
            self.logger.error(f"Lỗi Micro: {e}")
            # Lưu khẩn cấp khi có lỗi
            self._save_audio_buffer()
            self._save_transcript_temp()
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            # Lưu lần cuối trước khi đóng
            self._save_audio_buffer()
            self.logger.info("🔴 Microphone đã đóng")

    async def run(self):
        from google import genai
        
        # Khởi tạo Client - API key tự động đọc từ biến môi trường
        self.client = genai.Client()
        
        # Cấu hình theo mẫu Google: response_modalities và system_instruction
        config = {
            "response_modalities": ["AUDIO"],  # Yêu cầu Gemini trả về audio
            "system_instruction": self.get_system_instruction()
        }

        # Model ID: gemini-2.5-flash-native-audio-preview-12-2025
        model_id = "gemini-2.5-flash-native-audio-preview-12-2025"
        
        try:
            self.logger.info(f"🚀 Kết nối tới Gemini Live API... Model: {model_id}")

            async with self.client.aio.live.connect(
                model=model_id,
                config=config
            ) as session:
                self.is_listening = True
                self.session = session  # Lưu session vào instance
                self.logger.info(f"✅ Đã kết nối! Model: {model_id}")
                self.logger.info("🔴 Hà Vy đang lắng nghe... (Nói để gọi 'Hà Vy' hoặc 'Vy')")
                self.logger.info("⌨️ NHẤN PHÍM 'm' để yêu cầu biên bản cuối buổi họp")
                
                # Khởi động keyboard listener
                self.start_keyboard_listener()
                
                # Chạy đồng thời Gửi và Nhận
                await asyncio.gather(
                    self.send_microphone_audio(session),
                    self.receive_responses(session)
                )

        except Exception as e:
            # Xử lý các lỗi thông thường
            error_msg = str(e)
            if "1007" in error_msg:
                self.logger.error("❌ Lỗi 1007: Server không nhận diện được luồng âm thanh")
            elif "401" in error_msg or "Unauthorized" in error_msg:
                self.logger.error("❌ Lỗi xác thực: Kiểm tra GEMINI_API_KEY trong file .env")
            elif "403" in error_msg or "Forbidden" in error_msg:
                self.logger.error("❌ Lỗi quyền truy cập: API key không có quyền sử dụng Live API")
            elif "404" in error_msg or "Not Found" in error_msg:
                self.logger.error("❌ Lỗi model: Model không tồn tại hoặc không khả dụng")
            else:
                self.logger.error(f"❌ Lỗi: {e}")
        finally:
            self.is_listening = False
            if self.transcript_buffer:
                self.save_minutes()
            self.logger.info("🏁 Đã đóng phiên làm việc.")

if __name__ == "__main__":
    vy = MeetingMemberVy()
    print("--- TRỢ LÝ HÀ VY ĐANG KHỞI ĐỘNG ---")
    asyncio.run(vy.run())