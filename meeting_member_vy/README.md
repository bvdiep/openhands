# Meeting Member Vy - Thành viên Cuộc họp Thời gian Thực
!!! LƯU Ý: nhiều lỗi không dùng được.

Ứng dụng Python tạo thành viên cuộc họp thông minh sử dụng Gemini Flash 2.5 Native Audio (Multimodal Live API).

## 🎯 Tính năng

- **Lắng nghe thời gian thực**: Thu âm từ microphone hoặc xử lý file audio
- **Phát hiện tên thông minh**: Tự động phát hiện khi "Hạ Vy" hoặc "Vy" được gọi
- **Phản hồi tự nhiên**: Chỉ phản hồi khi được gọi tên, sử dụng tiếng Việt tự nhiên
- **Hệ thống log linh hoạt**: 3 mức độ log (production/info/debug)
- **Giao diện terminal thân thiện**: Hiển thị rõ ràng các sự kiện quan trọng

## 🛠️ Yêu cầu Hệ thống

### Phần mềm bắt buộc:
- Python 3.8+
- FFmpeg (để xử lý audio)

### Cài đặt FFmpeg:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Tải từ https://ffmpeg.org/download.html
- Thêm vào PATH

### Cài đặt PyAudio (cho microphone):

**Ubuntu/Debian:**
```bash
sudo apt install portaudio19-dev python3-dev
```

**macOS:**
```bash
brew install portaudio
```

**Windows:**
- PyAudio wheel sẽ được cài tự động

## 🚀 Cài đặt

### 1. Clone hoặc tải về dự án
```bash
git clone <repository-url>
cd meeting_member_vy
```

### 2. Tạo virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# hoặc
.venv\Scripts\activate     # Windows
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình API Key
```bash
# Sao chép file cấu hình mẫu
cp .env.example .env

# Chỉnh sửa file .env
nano .env
```

Thêm API key của bạn:
```env
GEMINI_API_KEY=your_actual_api_key_here
LOG_LEVEL=info
```

**Lấy API Key:**
1. Truy cập https://aistudio.google.com/app/apikey
2. Tạo API key mới
3. Sao chép và dán vào file `.env`

## 🎮 Sử dụng

### Chạy ứng dụng:
```bash
source .venv/bin/activate
python main.py
```

### Các chế độ log:

**Production Mode** (chỉ hiển thị khi Vy được gọi):
```bash
LOG_LEVEL=production python main.py
```

**Info Mode** (hiển thị transcript chính):
```bash
LOG_LEVEL=info python main.py
```

**Debug Mode** (hiển thị tất cả chi tiết):
```bash
LOG_LEVEL=debug python main.py
```

## 📋 Cách hoạt động

1. **Khởi động**: Ứng dụng kết nối tới Gemini Live API
2. **Lắng nghe**: Thu âm từ microphone hoặc xử lý file audio
3. **Phát hiện**: Theo dõi transcript để tìm "Hạ Vy" hoặc "Vy"
4. **Phản hồi**: Khi được gọi, Vy sẽ phản hồi phù hợp
5. **Hiển thị**: Chỉ hiển thị text trên terminal (không phát audio)

## 🎤 Xử lý Audio

### Định dạng hỗ trợ:
- **Input**: MP3, WAV, M4A, FLAC, và các định dạng phổ biến
- **Output**: PCM 16-bit 16kHz Mono (cho Gemini API)

### Microphone:
- Tự động phát hiện thiết bị audio
- Thu âm real-time với chất lượng cao
- Xử lý noise và echo cancellation

## 🔧 Cấu trúc Dự án

```
meeting_member_vy/
├── .venv/                 # Virtual environment
├── main.py               # Ứng dụng chính
├── audio_processor.py    # Module xử lý audio
├── requirements.txt      # Dependencies
├── .env.example         # File cấu hình mẫu
├── .env                 # File cấu hình (tạo từ .env.example)
└── README.md           # Hướng dẫn này
```

## 🎯 Ví dụ Sử dụng

### Khi chạy ứng dụng:
```
🤖 Ứng dụng Thành viên Cuộc họp - Hạ Vy
==================================================
🚀 Khởi tạo Hạ Vy - Meeting Member (Log level: info)
✅ Kết nối Gemini API thành công
🔗 Đang kết nối tới Gemini Live API...
✅ Kết nối Gemini Live API thành công
👂 Bắt đầu lắng nghe cuộc họp...
```

### Khi có người nói:
```
🎤 Chào mọi người, chúng ta bắt đầu cuộc họp nhé
🎤 Hôm nay chúng ta sẽ thảo luận về dự án mới
```

### Khi Vy được gọi:
```
🎤 Hạ Vy, bạn có ý kiến gì về vấn đề này không?

🔔 [14:30:25] Hạ Vy được gọi!

💬 [14:30:26] Vy: Vâng, tôi đang lắng nghe. Tôi nghĩ chúng ta nên xem xét thêm về khía cạnh kỹ thuật của dự án này.
📋 Hành động tiếp theo: Chuẩn bị báo cáo phân tích kỹ thuật
```

## 🐛 Xử lý Lỗi

### Lỗi thường gặp:

**1. GEMINI_API_KEY chưa được cấu hình:**
```
❌ GEMINI_API_KEY chưa được cấu hình trong file .env
```
→ Kiểm tra file `.env` và đảm bảo API key đúng

**2. PyAudio không cài được:**
```
❌ Lỗi cài đặt PyAudio
```
→ Cài đặt system dependencies:
```bash
# Ubuntu/Debian
sudo apt install portaudio19-dev python3-dev

# macOS
brew install portaudio
```

**3. FFmpeg không tìm thấy:**
```
❌ FFmpeg không có sẵn
```
→ Cài đặt FFmpeg theo hướng dẫn ở trên

**4. Microphone không hoạt động:**
```bash
# Test microphone
python -c "
from audio_processor import AudioProcessor
ap = AudioProcessor()
print('Devices:', ap.list_audio_devices())
print('Test result:', ap.test_microphone())
"
```

## 🔒 Bảo mật

- API key được lưu trong file `.env` (không commit vào git)
- Không ghi log API key hoặc dữ liệu nhạy cảm
- Audio chỉ được xử lý local, không lưu trữ

## 🤝 Đóng góp

1. Fork dự án
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Dự án này được phân phối dưới MIT License. Xem file `LICENSE` để biết thêm chi tiết.

## 🆘 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra phần "Xử lý Lỗi" ở trên
2. Chạy với `LOG_LEVEL=debug` để xem chi tiết
3. Tạo issue trên GitHub với log đầy đủ

---

**Phát triển bởi**: OpenHands AI Assistant  
**Phiên bản**: 1.0.0  
**Cập nhật**: 2024