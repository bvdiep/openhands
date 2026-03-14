import os
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.terminal import TerminalTool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.browser_use import BrowserToolSet

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
        Tool(name=BrowserToolSet.name)
    ],
)

# 3. Tạo cuộc hội thoại (Conversation)
# Tham số workspace trỏ đến thư mục dự án của bạn
cwd = "/home/dd/work/codes/HP/hp-lms-be"

conversation = Conversation(agent=agent, workspace=cwd)

# 4. Prompt xây dựng MCP Server
task_prompt = """
Nhiệm vụ: Tích hợp Swagger (OpenAPI) vào dự án NestJS và thực hiện kiểm chứng End-to-End (E2E) qua trình duyệt.
1. Khám phá & Cài đặt (Context Discovery):
- Quét toàn bộ mã nguồn để xác định các Controller, DTO và file entry point (thường là main.ts).
- Kiểm tra và cài đặt các package: @nestjs/swagger và swagger-ui-express.
- Cấu hình @nestjs/swagger plugin trong file nest-cli.json để tự động hóa việc mapping các thuộc tính DTO.

2. Cấu hình Code (Implementation):
- Tại main.ts, khởi tạo DocumentBuilder với:
    - Tiêu đề: "LMS API Documentation"
    - Route: /docs
    - Security: Thêm cấu hình addBearerAuth() để hỗ trợ JWT.
- Duyệt qua các Controller, thêm decorator @ApiTags để phân nhóm và @ApiOperation cho các endpoint chính.
- Thêm cả các decorators ghi tên của API để người dùng dễ nhận biết
- Đảm bảo các DTO được sử dụng đúng kiểu dữ liệu để Swagger hiển thị Schema chính xác.

3. Thông tin Xác thực (Credentials):
- Sử dụng thông tin sau để thực hiện các bài test yêu cầu bảo mật:
    - Username: admin@gmail.com
    - Password: 123456
- Nếu hệ thống yêu cầu đăng nhập để lấy Token, hãy thực hiện luồng này trước.

4. Kiểm chứng Trực quan bằng Browser (Validation Loop):
- Khởi chạy server bằng lệnh npm run start:dev (hoặc lệnh tương đương trong dự án).
- Sử dụng Browser Tool:
    - Truy cập http://localhost:3132/docs.
    - Chụp ảnh màn hình toàn cảnh giao diện Swagger UI để báo cáo.
    - Thực hiện luồng Login (nếu cần) trên giao diện web để lấy JWT, sau đó dán vào nút "Authorize" của Swagger.
    - Chọn ngẫu nhiên một API thuộc nhóm "Protected" (yêu cầu login), thực hiện "Try it out" và nhấn "Execute".
    - Xác nhận Response Code trả về là 200 hoặc 201.

5. Điều kiện Hoàn thành (Definition of Done):
- Dự án phải build thành công (npm run build).
- Swagger UI phải hiển thị đầy đủ các Endpoint đã quét được.
- Ít nhất một API test có Authentication phải thành công thông qua Browser Tool.
- Để lại một file swagger-report.md tóm tắt các bước đã làm và đính kèm đường dẫn ảnh chụp màn hình.
"""

print(f"🚀 OpenHands SDK V1 đang khởi chạy tại: {cwd}")

# 5. Chạy nhiệm vụ
try:
    conversation.send_message(task_prompt)
    # Trong SDK V1, dùng .run() để Agent thực hiện chuỗi hành động cho đến khi xong
    conversation.run() 
    print("\n✅ Nhiệm vụ hoàn tất! Kiểm tra code")
except Exception as e:
    print(f"❌ Lỗi thực thi: {e}")