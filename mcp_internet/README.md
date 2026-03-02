# MCP Internet Search Server

MCP Server cung cấp khả năng tìm kiếm internet với pipeline: Serper (Search) → VoyageAI (Rerank) → Trafilatura (Extract Clean Content).

## Tính năng

- ✅ **Tìm kiếm**: Sử dụng Serper API để tìm kiếm trên Google
- ✅ **Rerank**: Sử dụng VoyageAI rerank-2.5 để sắp xếp lại kết quả theo độ liên quan
- ✅ **Crawl & Extract**: Sử dụng httpx để crawl và Trafilatura để trích xuất nội dung sạch
- ✅ **Lọc**: Tự động loại bỏ các link từ YouTube, Facebook, Instagram

## Yêu cầu hệ thống

- Python 3.8+
- Internet connection (để tìm kiếm và crawl)

## Cài đặt

### 1. Tạo virtual environment

```bash
cd mcp_internet
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# hoặc .venv\Scripts\activate  # Windows
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình API Keys

Tạo file `.env` trong thư mục gốc với nội dung:

```env
SERPER_API_KEY=your_serper_api_key_here
VOYAGE_API_KEY=your_voyage_api_key_here
```

### 4. Lấy API Keys

#### Serper API
1. Truy cập: https://serper.dev/
2. Đăng ký tài khoản
3. Lấy API key từ dashboard

#### VoyageAI API
1. Truy cập: https://www.voyageai.com/
2. Đăng ký tài khoản
3. Lấy API key từ dashboard

## Cách sử dụng

> **⚠️ Lưu ý quan trọng:** Cần phân biệt giữa:
> - **Giao thức MCP**: Sử dụng MCP client/server để giao tiếp qua stdio
> - **Gọi trực tiếp hàm**: Import và gọi hàm Python trực tiếp (không qua MCP)

---

### A. Sử dụng GIAO THỨC MCP (khuyến nghị)

#### Cách 1: Tích hợp với Claude Desktop

Thêm cấu hình vào file `claude_desktop_config.json`:

#### Windows
Đường dẫn: `%APPDATA%\Claude\claude_desktop_config.json`

#### macOS
Đường dẫn: `~/Library/Application Support/Claude/claude_desktop_config.json`

#### Linux
Đường dẫn: `~/.config/Claude/claude_desktop_config.json`

**Nội dung cấu hình:**
```json
{
  "mcpServers": {
    "internet-search": {
      "command": "python",
      "args": ["/đường/dẫn/đến/mcp_internet/server.py"],
      "env": {
        "SERPER_API_KEY": "your_serper_api_key_here",
        "VOYAGE_API_KEY": "your_voyage_api_key_here"
      }
    }
  }
}
```

Sau đó khởi động lại Claude Desktop và sử dụng tool `internet_search_tool`.

#### Cách 2: Từ Python code (StdioServerParameters)

Sử dụng `StdioServerParameters` để tích hợp MCP server vào ứng dụng Python:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def internet_search(query: str, max_results: int = 5):
    """Tìm kiếm internet qua MCP server"""
    server_params = StdioServerParameters(
        command="python",
        args=["/đường/dẫn/đến/mcp_internet/server.py"],
        env={
            "SERPER_API_KEY": "your_serper_api_key",
            "VOYAGE_API_KEY": "your_voyage_api_key"
        }
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool(
                "internet_search_tool",
                {"query": query, "max_results": max_results}
            )
            
            return result.content[0].text

# Sử dụng
result = asyncio.run(internet_search("Python MCP tutorial"))
print(result)
```

---

### B. Gọi trực tiếp hàm (không qua MCP)

#### Cách 1: HTTP API (FastAPI)

Bạn có thể tạo một HTTP wrapper để kết nối từ các chatbot khác:

```python
# http_server.py
# HTTP server wrapper cho MCP Internet Search

import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import sys
from pathlib import Path

# Thêm đường dẫn server vào sys.path
sys.path.insert(0, str(Path(__file__).parent))

from server import internet_search_tool

app = FastAPI(title="MCP Internet Search API")

class SearchRequest(BaseModel):
    query: str
    max_results: int = 5

@app.get("/")
async def root():
    return {"message": "MCP Internet Search API", "version": "1.0.0"}

@app.post("/search")
async def search(request: SearchRequest):
    try:
        result = await internet_search_tool(
            query=request.query,
            max_results=request.max_results
        )
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Chạy server:**
```bash
pip install fastapi uvicorn
python http_server.py
```

**Sử dụng API:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence trends 2024", "max_results": 5}'
```

### Cách 2: Tích hợp vào Telegram Bot

```python
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import MCP server function
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from server import internet_search_tool

async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("🔍 Đang tìm kiếm...")
    
    result = await internet_search_tool(query=query, max_results=5)
    await update.message.reply_text(result)

async def main():
    application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))
    
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### Tool: `internet_search_tool`

**Input:**
| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `query` | string | ✅ | Từ khóa tìm kiếm |
| `max_results` | integer | ❌ | Số kết quả tối đa (mặc định: 5, tối đa: 10) |

**Output:**
String chứa kết quả tìm kiếm với:
- Title của mỗi kết quả
- URL
- Relevance score
- Snippet
- Nội dung được trích xuất (tối đa 2000 ký tự)

## Cấu trúc Pipeline

```
1. Serper Search       → Tìm kiếm 10 kết quả đầu tiên từ Google
2. Domain Filter      → Loại bỏ YouTube, Facebook, Instagram
3. VoyageAI Rerank    → Sắp xếp lại theo độ liên quan với query
4. Content Crawl     → Crawl nội dung từ các URL được chọn
5. Trafilatura Extract → Trích xuất text sạch, loại bỏ HTML/ads
6. Format Output      → Định dạng kết quả cuối cùng
```

## Troubleshooting

### 1. Lỗi "Missing required API keys"
- Kiểm tra file `.env` có tồn tại và đúng format
- Đảm bảo API keys hợp lệ

### 2. Lỗi timeout khi crawl
- Tăng giá trị `HTTP_TIMEOUT` trong `server.py` (mặc định: 10.0)
- Một số website có thể chặn bot, đây là hành vi bình thường

### 3. Không crawl được nội dung
- Một số website có cơ chế chống bot
- Thử tăng User-Agent trong code

### 4. Lỗi Serper API
- Kiểm tra quota API còn hạn
- Xác nhận API key đúng

### 5. Lỗi VoyageAI Rerank
- Kiểm tra API key có quyền rerank
- Model "rerank-2.5" cần được enable trong tài khoản

## Giới hạn

- **Serper**: 2 (free tier)
- **,500 requests/monthVoyageAI**: Theo gói subscription
- **Content length**: Tối đa 2000 ký tự mỗi kết quả
- **max_results**: Tối đa 10 kết quả

## Cấu trúc Project

```
mcp_internet/
├── .env                  # API keys
├── .venv/                # Virtual environment
├── server.py             # MCP Server chính
├── requirements.txt      # Dependencies
├── claude_desktop_config.json  # Claude Desktop config
└── README.md             # Tài liệu này
```

## License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push và tạo Pull Request
