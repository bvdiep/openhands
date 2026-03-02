# Meeting Audio Transcription MCP Server

Một MCP (Model Context Protocol) Server để chuyển đổi âm thanh cuộc họp thành văn bản sử dụng Groq API với tính năng smart chunking cho file lớn.

## Tính năng

- ✅ Hỗ trợ nhiều định dạng âm thanh: `.ogg`, `.mp3`, `.wav`, `.m4a`, `.flac`, `.aac`
- ✅ Smart chunking: Tự động chia file lớn (>25MB) thành các đoạn 10 phút
- ✅ Sử dụng Groq API với model `whisper-large-v3` cho chất lượng transcription cao
- ✅ Xử lý bất đồng bộ (async) để không làm treo server
- ✅ Tự động dọn dẹp file tạm thời
- ✅ Xử lý lỗi toàn diện (file không tồn tại, lỗi API, rate limit)

## Yêu cầu hệ thống

### 1. FFmpeg (Bắt buộc)

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
1. Tải FFmpeg từ https://ffmpeg.org/download.html
2. Giải nén và thêm vào PATH
3. Hoặc sử dụng chocolatey: `choco install ffmpeg`

### 2. Python 3.8+

Đảm bảo bạn có Python 3.8 trở lên.

## Cài đặt

### 1. Clone repository và setup môi trường

```bash
cd /path/to/your/project
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# hoặc .venv\Scripts\activate  # Windows
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình môi trường

Tạo file `.env` trong thư mục gốc:

```env
GROQ_API_KEY="your_groq_api_key_here"
```

**Lấy Groq API Key:**
1. Đăng ký tại https://console.groq.com/
2. Tạo API key mới
3. Copy và paste vào file `.env`

## Sử dụng

### 1. Chạy MCP Server

```bash
source .venv/bin/activate
python server.py
```

### 2. Tích hợp với Claude Desktop

Thêm vào file cấu hình Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json` trên macOS hoặc `%APPDATA%\Claude\claude_desktop_config.json` trên Windows):

```json
{
  "mcpServers": {
    "meeting-transcription": {
      "command": "python",
      "args": ["/absolute/path/to/your/project/server.py"],
      "cwd": "/absolute/path/to/your/project",
      "env": {
        "PATH": "/absolute/path/to/your/project/.venv/bin:/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

### 3. Tích hợp với Telegram Bot Backend

```python
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def transcribe_meeting_audio(file_path: str):
    server_params = StdioServerParameters(
        command="python",
        args=["/path/to/your/server.py"],
        cwd="/path/to/your/project",
        env={"GROQ_API_KEY": "your_api_key"}
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool(
                "transcribe_meeting",
                arguments={"file_path": file_path}
            )
            
            return json.loads(result.content[0].text)

# Sử dụng trong Telegram bot
async def handle_audio_message(update, context):
    # Download audio file từ Telegram
    file_path = await download_telegram_audio(update.message.audio)
    
    # Transcribe
    result = await transcribe_meeting_audio(file_path)
    
    # Gửi kết quả
    await update.message.reply_text(f"Transcript: {result['full_transcript']}")
```

## API Reference

### Tool: `transcribe_meeting`

**Input:**
```json
{
  "file_path": "/absolute/path/to/audio/file.mp3"
}
```

**Output:**
```json
{
  "full_transcript": "Nội dung văn bản đầy đủ của cuộc họp...",
  "duration_seconds": 1800.5,
  "file_info": {
    "original_file": "/path/to/file.mp3",
    "format": "mp3",
    "size_mb": 45.2,
    "chunks_processed": 3
  }
}
```

## Xử lý lỗi

Server xử lý các lỗi phổ biến:

- **File không tồn tại**: Trả về lỗi với thông báo rõ ràng
- **Định dạng không hỗ trợ**: Liệt kê các định dạng được hỗ trợ
- **Lỗi Groq API**: Bao gồm rate limit, network issues
- **Lỗi xử lý âm thanh**: Fallback giữa librosa và pydub

## Hiệu suất

- **File nhỏ (<25MB)**: Xử lý trực tiếp, thời gian ~1-2 phút
- **File lớn (>25MB)**: Tự động chia thành chunks 10 phút, xử lý song song
- **Memory usage**: Tối ưu với việc dọn dẹp file tạm thời tự động

## Troubleshooting

### 1. Lỗi FFmpeg không tìm thấy
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```
**Giải pháp**: Cài đặt FFmpeg theo hướng dẫn ở trên.

### 2. Lỗi Groq API Key
```
Error: GROQ_API_KEY not found in environment variables
```
**Giải pháp**: Kiểm tra file `.env` và đảm bảo API key đúng.

### 3. Lỗi import librosa
```
ImportError: librosa requires ffmpeg
```
**Giải pháp**: Cài đặt FFmpeg và restart terminal.

### 4. File quá lớn
Server tự động xử lý file lớn bằng chunking. Nếu vẫn gặp lỗi memory, giảm `CHUNK_DURATION_MINUTES` trong `server.py`.

## Development

### Chạy tests
```bash
source .venv/bin/activate
python -m pytest tests/
```

### Logging
Server in log ra console. Để debug, chạy với verbose:
```bash
python server.py --verbose
```

## License

MIT License - xem file LICENSE để biết thêm chi tiết.

## Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Tạo Pull Request

## Support

Nếu gặp vấn đề, vui lòng tạo issue trên GitHub với thông tin:
- Hệ điều hành
- Python version
- Error message đầy đủ
- File audio sample (nếu có thể)