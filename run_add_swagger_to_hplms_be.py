from openhands_v2.runner import run_task

# 1. Cấu hình
cwd = "/home/dd/work/codes/HP/hp-lms-be"

# 2. Nhiệm vụ
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

# 3. Chạy nhiệm vụ
if __name__ == "__main__":
    run_task(
        task_prompt=task_prompt,
        workspace=cwd,
        model="openai/sonnet-4",
        success_message="Nhiệm vụ hoàn tất! Kiểm tra code"
    )
