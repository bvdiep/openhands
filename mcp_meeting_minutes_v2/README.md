# MCP Meeting Minutes Server

MCP Server để xử lý âm thanh cuộc họp bằng Gemini Multimodal Live API với hỗ trợ transcription và speaker diarization cho tiếng Việt.

## Tính năng

- ✅ Transcribe âm thanh cuộc họp với độ chính xác cao cho tiếng Việt
- ✅ Speaker Diarization (phân biệt người nói)
- ✅ Nhận diện thuật ngữ kỹ thuật và từ lóng
- ✅ Sử dụng Gemini 2.5 Flash API với hỗ trợ multimodal (audio + text)
- ✅ Hỗ trợ nhiều định dạng audio (MP3, WAV, M4A, etc.)

## Yêu cầu hệ thống

### Phần mềm bắt buộc
- Python 3.8+
- **FFmpeg** (bắt buộc cho xử lý audio)

### Cài đặt FFmpeg

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS:
```bash
brew install ffmpeg
```

#### Windows:
1. Tải FFmpeg từ https://ffmpeg.org/download.html
2. Giải nén và thêm vào PATH
3. Hoặc sử dụng chocolatey: `choco install ffmpeg`

## Cài đặt

### 1. Clone repository và cài đặt dependencies

```bash
cd mcp_meeting_minutes_v2
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# hoặc .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Cấu hình API Key

Tạo file `.env` trong thư mục gốc:

```env
GEMINI_API_KEY="your_gemini_api_key_here"
```

**Lấy API Key:**
1. Truy cập [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Tạo API key mới
3. Copy và paste vào file `.env`

### 3. Kiểm tra cài đặt

```bash
source .venv/bin/activate
python server.py
```

Nếu không có lỗi, server đã sẵn sàng sử dụng.

## Sử dụng

### Tool: `transcribe_meeting_native`

**Input:**
- `file_path`: Đường dẫn tuyệt đối đến file âm thanh

**Output:**
```json
{
  "full_transcript": "Nội dung đầy đủ của cuộc họp",
  "speakers": [
    {
      "speaker_id": "Speaker_1",
      "segments": [
        {
          "start_time": "00:00:00",
          "end_time": "00:00:10",
          "text": "Nội dung người nói"
        }
      ]
    }
  ]
}
```

## Tích hợp

### Claude Desktop

Thêm vào file cấu hình Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "meeting-transcriber": {
      "command": "python",
      "args": ["/path/to/mcp_meeting_minutes_v2/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/mcp_meeting_minutes_v2/.venv/lib/python3.x/site-packages"
      }
    }
  }
}
```

### Telegram Bot

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def transcribe_audio(file_path: str):
    server_params = StdioServerParameters(
        command="python",
        args=["/path/to/server.py"],
        env={"PYTHONPATH": "/path/to/.venv/lib/python3.x/site-packages"}
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool(
                "transcribe_meeting_native",
                {"file_path": file_path}
            )
            
            return result.content[0].text
```

## Định dạng audio được hỗ trợ

- MP3
- WAV
- M4A
- FLAC
- OGG
- AAC
- WMA

Audio sẽ được tự động chuyển đổi về PCM 16-bit 16kHz mono để tối ưu cho Gemini Live API.

## Troubleshooting

### Lỗi "FFmpeg not found"
- Đảm bảo FFmpeg đã được cài đặt và có trong PATH
- Kiểm tra: `ffmpeg -version`

### Lỗi "GEMINI_API_KEY not found"
- Kiểm tra file `.env` có tồn tại và chứa API key
- Đảm bảo API key hợp lệ

### Lỗi "File not found"
- Sử dụng đường dẫn tuyệt đối cho file audio
- Kiểm tra file có tồn tại và có quyền đọc

### Lỗi kết nối Gemini API
- Kiểm tra kết nối internet
- Xác nhận API key còn hạn sử dụng
- Kiểm tra quota API (1M TPM cho Live API)

## Giới hạn

- **Quota:** Theo giới hạn của Gemini API (thường là 15 requests/minute cho free tier)
- **File size:** Tối đa 20MB per file (khuyến nghị)
- **Duration:** Tối đa 60 phút per file (khuyến nghị)
- **Language:** Tối ưu cho tiếng Việt, hỗ trợ tiếng Anh

## Phát triển

### Cấu trúc project
```
mcp_meeting_minutes_v2/
├── .env                 # API keys
├── .venv/              # Virtual environment
├── server.py           # MCP server chính
├── requirements.txt    # Dependencies
└── README.md          # Tài liệu này
```

### Logging
Server sử dụng Python logging với level INFO. Để debug:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push và tạo Pull Request

## Liên hệ

- GitHub Issues: [Tạo issue mới](https://github.com/your-repo/issues)
- Email: your-email@example.com