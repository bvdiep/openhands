# HP LMS BE Technical Documentation Pipeline

Hệ thống tự động tạo tài liệu kỹ thuật cho HP LMS Backend System sử dụng OpenHands Pipeline Framework.

## 📋 Tổng quan

Pipeline này tự động phân tích và tạo ra tài liệu kỹ thuật toàn diện cho hệ thống HP LMS BE, bao gồm:

- **Architecture Documentation**: Tài liệu kiến trúc hệ thống, module structure, design patterns
- **API Specification**: Tài liệu chi tiết các REST endpoints, request/response schemas
- **Database Schema**: Tài liệu cơ sở dữ liệu, entity relationships, constraints

## 🎯 Mục tiêu

- Tự động hóa việc tạo tài liệu kỹ thuật từ source code
- Đảm bảo tài liệu luôn đồng bộ với code thực tế
- Tạo ra tài liệu chất lượng cao, dễ đọc và dễ bảo trì
- Hỗ trợ Quarto processing cho xuất bản đa định dạng

## 🏗️ Cấu trúc Pipeline

### Step 1: Planning and Analysis
- Phân tích cấu trúc codebase HP LMS BE
- Lập kế hoạch chi tiết cho việc tạo tài liệu
- Xác định các component chính và mối quan hệ

### Step 2: Architecture Documentation
- Tạo tài liệu kiến trúc hệ thống
- Mô tả module structure và dependencies
- Tạo các biểu đồ kiến trúc bằng Mermaid

### Step 3: API Specification
- Tài liệu hóa tất cả REST endpoints
- Mô tả request/response schemas
- Tạo API flow diagrams

### Step 4: Database Schema
- Tài liệu hóa database schema
- Tạo ER diagrams cho entity relationships
- Mô tả constraints và indexes

### Step 5: Quality Assurance
- Kiểm tra chất lượng tài liệu
- Đảm bảo tính nhất quán và đầy đủ
- Hoàn thiện và tối ưu hóa

## 🚀 Sử dụng

### Chạy toàn bộ pipeline:
```bash
python pipeline.py run all
```

### Chạy từng step:
```bash
python pipeline.py run 1    # Planning and Analysis
python pipeline.py run 2    # Architecture Documentation
python pipeline.py run 3    # API Specification
python pipeline.py run 4    # Database Schema
python pipeline.py run 5    # Quality Assurance
```

### Chạy một dải steps:
```bash
python pipeline.py run 1 3  # Chạy steps 1-3
```

### Liệt kê các steps:
```bash
python pipeline.py list
```

## 📁 Cấu hình

### Project Configuration
- **Project Name**: `hplmsbe_techdoc`
- **Workspace**: `hplmsbe_techdoc`
- **Target Codebase**: `/home/dd/work/codes/HP/hp-lms-be`
- **Model**: `openai/local-gemini-3-flash` (LiteLLM proxy)

### Output Format
- **Format**: Markdown với Mermaid diagrams
- **Compatibility**: Quarto-ready
- **Structure**: Hierarchical với cross-references

## 🔧 Yêu cầu kỹ thuật

- OpenHands Pipeline Framework
- LiteLLM proxy với Gemini Flash model
- Access đến HP LMS BE codebase
- Quarto (optional, cho publishing)

## 📝 Output Files

Sau khi chạy xong, pipeline sẽ tạo ra:

- `architecture-documentation.md` - Tài liệu kiến trúc hệ thống
- `api-specification.md` - Tài liệu API specification
- `database-schema.md` - Tài liệu database schema
- `quality-assurance-report.md` - Báo cáo QA
- `README.md` - Hướng dẫn sử dụng tài liệu

## 🎨 Features

- **Automatic Code Analysis**: Tự động phân tích NestJS/TypeScript codebase
- **Mermaid Diagrams**: Tạo biểu đồ trực quan embedded trong Markdown
- **Quarto Compatible**: Sẵn sàng cho xuất bản đa định dạng
- **Quality Assurance**: Kiểm tra và đảm bảo chất lượng tự động
- **Modular Design**: Có thể chạy từng step độc lập

## 📚 Tài liệu tham khảo

- [OpenHands Documentation](https://docs.openhands.dev/)
- [Mermaid Documentation](https://mermaid.js.org/)
- [Quarto Documentation](https://quarto.org/)
- [NestJS Documentation](https://nestjs.com/)

---

*Được tạo bởi OpenHands Pipeline Framework cho HP LMS BE Technical Documentation*