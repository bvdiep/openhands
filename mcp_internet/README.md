# MCP Internet Search Server

MCP Server cung cấp khả năng tìm kiếm internet với pipeline: Serper (Search) → VoyageAI (Rerank) → Trafilatura (Extract Clean Content).

## Tính năng

- **Tìm kiếm**: Sử dụng Serper API để tìm kiếm trên Google
- **Rerank**: Sử dụng VoyageAI rerank-2.5 để sắp xếp lại kết quả theo độ liên quan
- **Crawl & Extract**: Sử dụng httpx để crawl và Trafilatura để trích xuất nội dung sạch
- **Lọc**: Tự động loại bỏ các link từ YouTube, Facebook, Instagram

## Cài đặt

1. **Tạo virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# hoặc .venv\Scripts\activate  # Windows
```

2. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

3. **Cấu hình API Keys:**
Tạo file `.env` với nội dung:
```
SERPER_API_KEY=your_serper_api_key_here
VOYAGE_API_KEY=your_voyage_api_key_here
```

## Cấu hình Claude Desktop

Thêm cấu hình sau vào file `claude_desktop_config.json`:

### Windows
Đường dẫn: `%APPDATA%\Claude\claude_desktop_config.json`

### macOS
Đường dẫn: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Linux
Đường dẫn: `~/.config/Claude/claude_desktop_config.json`

**Nội dung cấu hình:**
```json
{
  "mcpServers": {
    "internet-search": {
      "command": "python",
      "args": ["/đường/dẫn/đến/thư/mục/server.py"],
      "env": {
        "SERPER_API_KEY": "your_serper_api_key_here",
        "VOYAGE_API_KEY": "your_voyage_api_key_here"
      }
    }
  }
}
```

**Lưu ý:** Thay `/đường/dẫn/đến/thư/mục/server.py` bằng đường dẫn tuyệt đối đến file `server.py` của bạn.

## Sử dụng

Sau khi cấu hình, khởi động lại Claude Desktop. Bạn có thể sử dụng tool `internet_search_tool` với các tham số:

- `query` (bắt buộc): Từ khóa tìm kiếm
- `max_results` (tùy chọn): Số lượng kết quả tối đa (mặc định: 5, tối đa: 10)

**Ví dụ:**
```
Tìm kiếm thông tin về "artificial intelligence trends 2024"
```

## Kiểm tra

Chạy lệnh sau để kiểm tra server:
```bash
python server.py
```

Server sẽ chạy ở chế độ stdio và chờ input từ MCP client.

## API Keys

### Serper API
1. Truy cập: https://serper.dev/
2. Đăng ký tài khoản
3. Lấy API key từ dashboard

### VoyageAI API
1. Truy cập: https://www.voyageai.com/
2. Đăng ký tài khoản
3. Lấy API key từ dashboard

## Troubleshooting

1. **Lỗi "Missing required API keys"**: Kiểm tra file `.env` có đúng format và API keys hợp lệ
2. **Lỗi timeout**: Tăng giá trị `HTTP_TIMEOUT` trong `server.py`
3. **Không crawl được nội dung**: Một số website có thể chặn bot, đây là hành vi bình thường

## Cấu trúc Pipeline

1. **Serper Search**: Tìm kiếm 10 kết quả đầu tiên từ Google
2. **Domain Filter**: Loại bỏ YouTube, Facebook, Instagram
3. **VoyageAI Rerank**: Sắp xếp lại theo độ liên quan với query
4. **Content Crawl**: Crawl nội dung từ các URL được chọn
5. **Trafilatura Extract**: Trích xuất text sạch, loại bỏ HTML/ads
6. **Format Output**: Định dạng kết quả cuối cùng