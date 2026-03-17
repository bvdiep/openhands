# Healthcare BE Technical Documentation Pipeline

Hệ thống tự động tạo tài liệu kỹ thuật cho backend của nền tảng Healthcare.

## Mục tiêu

Tự động tạo ra tài liệu kỹ thuật chuyên nghiệp cho hệ thống Healthcare BE bao gồm:

- **Architecture Documentation**: Tài liệu kiến trúc hệ thống
- **API Specification**: Tài liệu đặc tả API
- **Database Schema**: Tài liệu cơ sở dữ liệu

## Cấu trúc Pipeline

### Step 1: Planning and Analysis
- Phân tích codebase Healthcare BE
- Lập kế hoạch tạo tài liệu
- Xác định cấu trúc và thành phần chính

### Step 2: Architecture Documentation
- Tạo tài liệu kiến trúc hệ thống
- Mô tả các module và component
- Tạo sơ đồ kiến trúc bằng Mermaid

### Step 3: API Specification
- Tài liệu hóa tất cả API endpoints
- Mô tả request/response formats
- Tài liệu authentication và authorization

### Step 4: Database Schema
- Tài liệu hóa database schema
- Mô tả entity relationships
- Tạo ERD diagrams bằng Mermaid

### Step 5: Quality Assurance
- Kiểm tra chất lượng tài liệu
- Đảm bảo tính nhất quán và đầy đủ
- Tạo báo cáo QA

## Cách sử dụng

### Liệt kê các steps
```bash
python pipeline.py list
```

### Chạy một step cụ thể
```bash
python pipeline.py run 1  # Chạy Step 1
```

### Chạy nhiều steps
```bash
python pipeline.py run 1 3  # Chạy Steps 1-3
```

### Chạy toàn bộ pipeline
```bash
python pipeline.py run all
```

## Cấu hình

- **Target codebase**: `/home/dd/work/codes/HEALTHCARE/healthcare-api`
- **Model sử dụng**: `gemini/gemini-3-flash-preview`
- **Output format**: Markdown với Mermaid diagrams
- **Workspace**: `hcbe_techdoc`

## Đặc điểm kỹ thuật

- Tự động bỏ qua files trong `.gitignore`
- Sử dụng Mermaid diagrams nhúng trực tiếp trong Markdown
- Tương thích với Quarto để render
- Tài liệu có cấu trúc chuyên nghiệp với table of contents
- Kiểm tra chất lượng tự động

## Output Files

Sau khi chạy pipeline, các file tài liệu sẽ được tạo trong workspace:

- `01_Architecture.md` - Tài liệu kiến trúc
- `02_API_Specification.md` - Đặc tả API
- `03_Database_Schema.md` - Schema cơ sở dữ liệu
- `QA_Report.md` - Báo cáo kiểm tra chất lượng

## Yêu cầu hệ thống

- Python 3.8+
- OpenHands framework
- Gemini API access
- Healthcare BE codebase tại đường dẫn chỉ định