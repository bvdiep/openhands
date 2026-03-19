import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runner import run_task
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1. Cấu hình
cwd = "/home/dd/work/diep/openhands/apps/documents_hc"
be_root = "/home/dd/work/codes/HEALTHCARE/healthcare-api"

# 2. Nhiệm vụ
task_prompt = f"""
Bạn đóng vai trò là một Solution Architect chuyên về hệ thống AI Agent, hỗ trợ tôi cập nhật tài liệu SRS (Software Requirements Specification) cho dự án.
Nhiệm vụ của bạn là chuẩn bị "vùng đệm dữ liệu" bằng cách chuyển đổi tài liệu cũ và lọc mã nguồn thực tế để đối chiếu nghiệp vụ.

Dữ liệu đầu vào:
- Tài liệu gốc: {cwd}/docs/SRS_V3.docx
- Ghi chú cập nhật: {cwd}/docs/Change_Notes.docx
- Mã nguồn Backend của dự án tại thư mục {be_root}.

Hãy thực hiện quy trình chuẩn bị sau:

### BƯỚC 1: CHUYỂN ĐỔI TÀI LIỆU (WORD TO MARKDOWN)
Sử dụng công cụ `pandoc` hệ thống để thực hiện:
1. Chuyển đổi `SRS_V3.docx` sang `SRS_V3.md` và `Change_Notes.docx` sang `Change_Notes.md` và để trong cùng thư mục {cwd}/docs/.
2. Sử dụng tham số `--extract-media={cwd}/docs/assets` để trích xuất toàn bộ hình ảnh, sơ đồ từ file Word ra thư mục assets.
3. Sau khi chuyển đổi, hãy đọc lướt qua các file .md để đảm bảo cấu trúc bảng biểu và đường dẫn hình ảnh (`![]({cwd}/docs/assets/media/...)`) đã được giữ lại chính xác.

### BƯỚC 2: CHUẨN BỊ VÙNG ĐỆM MÃ NGUỒN (CONTEXT PREPARATION)
1. Tạo thư mục {cwd}/codes (Xóa sạch nội dung nếu thư mục này đã tồn tại).
2. Dựa trên nội dung của `SRS_V3` và `Change_Notes.md`, hãy quét dự án gốc và copy các file "Sống" (chứa logic nghiệp vụ) vào {cwd}/codes, giữ nguyên cấu trúc thư mục cha:
   - **Data Layer:** Entities, Models, DTOs, Database Schemas.
   - **Logic Layer:** Các Services, UseCases, Business Logic xử lý các nghiệp vụ được nhắc đến trong SRS_V3 và Change_Notes. Có thể bỏ qua các phần không hề liên quan.
   - **Interface Layer:** Controllers, API Definitions (Swagger/Proto), Routes.
3. **Loại trừ tuyệt đối:** node_modules, vendor, bin, obj, .git, các file test (.spec, .test), file logs và các file cấu hình hạ tầng (Dockerfile, .env).

### BƯỚC 3: PHÂN TÍCH & ĐỐI CHIẾU BAN ĐẦU
1. Đọc mã nguồn trong {cwd}/codes và so sánh với mô tả trong `SRS_V3.md`.
2. Liệt kê danh sách các "Gap" (điểm khác biệt) giữa Code hiện tại và Tài liệu cũ.
3. Xác định các phần trong `Change_Notes.md` đã được cài đặt trong code hay chưa.

### BƯỚC 4: BÁO CÁO KẾT QUẢ
1. Hiển thị cây thư mục (tree) của thư mục {cwd}/codes lưu vào file {cwd}/code_tree.txt để tôi kiểm tra danh sách file bạn đã chọn.
2. Liệt kê danh sách các hình ảnh đã trích xuất được trong `{cwd}/docs/assets/media` lưu vào file {cwd}/media_tree.txt.
3. Xác nhận bạn đã sẵn sàng để bắt đầu viết lại các chương tương ứng trong SRS dưới dạng Markdown (SRS_V4.md).
"""

# 3. Chạy nhiệm vụ
if __name__ == "__main__":
    run_task(
        task_prompt=task_prompt,
        workspace=cwd,
        model="gemini/gemini-3.1-pro-preview",
        api_key=os.getenv("GEMINI_API_KEY", "no-gemini-api-key"),  # Fails fast if not set
        base_url=None,
        success_message="Nhiệm vụ hoàn tất! Kiểm tra code"
    )
