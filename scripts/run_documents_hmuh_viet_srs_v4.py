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
**Vai trò:** Bạn là một **Solution Architect** kiêm **Business Analyst** cao cấp. Nhiệm vụ của bạn là cập nhật nội dung chi tiết cho file `{cwd}/docs/SRS_V4.md` dựa trên các thay đổi thực tế từ mã nguồn và các ghi chú mới trong file `{cwd}/docs/Change_Notes.md`.

**Dữ liệu đầu vào hiện có:**

1. **Source of Truth (Mã nguồn):** Các file code cốt lõi đã được lọc tại `{cwd}/codes`.
2. **Yêu cầu thay đổi:** File `{cwd}/docs/Change_Notes.md`.
3. **Tài liệu tham chiếu gốc:** `{cwd}/docs/SRS_V3.md` (và bản gốc `{cwd}/docs/SRS_V3.docx` để xem hình ảnh). **CHÚ Ý**: đây là tài liệu đã thể hiện bộ khung của các thay đổi trong Change_Notes.docx và chúng ta cần cập nhật chi tiết cho những phần thay đổi này.
4. Có thể tham chiếu cả `{cwd}/docs/Change_Notes.docx nếu cần thiết. 

**Yêu cầu thực hiện:**

#### 1. Đối chiếu và Cập nhật Logic

Hãy đọc file `{cwd}/docs/SRS_V4.md` và thực hiện các chỉnh sửa trực tiếp vào file này:

- **Cập nhật tính năng:** Dựa trên `Change_Notes.md`, hãy **viết lại** hoặc **bổ sung chi tiết** tương ứng trong mỗi phần liên quan.
- **Xác thực với Code:** Đối chiếu với mã nguồn trong `{cwd}/codes`. Nếu tài liệu cũ mô tả một đằng nhưng code thực tế triển khai một nẻo, hãy cập nhật tài liệu theo **Logic của Code**.
- **Ràng buộc nghiệp vụ (Business Rules):** Cập nhật chính xác các điều kiện Validation, luồng xử lý dữ liệu từ tầng Service/Logic trong code vào tài liệu.

#### 2. Hướng dẫn xử lý hình ảnh & Tài liệu gốc

- Khi gặp các thẻ ảnh trong bản Markdown (ví dụ: `![image1]`), hãy đối chiếu với hình ảnh tương ứng trong file gốc `{cwd}/docs/SRS_V3.docx`.
- Nếu hình ảnh cũ không còn phù hợp với logic code mới, hãy để lại một ghi chú (Comment) ngay dưới ảnh đó trong file Markdown theo định dạng: \`\`.

#### 3. Nguyên tắc chỉnh sửa (Để tối ưu Git Diff)

- Chỉ sửa đổi những phần có sự thay đổi về nghiệp vụ hoặc logic.
- Giữ nguyên cấu trúc văn phong và định dạng của các phần không thay đổi để tôi dễ dàng kiểm tra qua `git diff`.
- Không tự ý thay đổi các ID của yêu cầu (ví dụ: `REQ-01`, `UC-02`) trừ khi có yêu cầu thay đổi cụ thể.

#### 4. Báo cáo sau khi hoàn thành

Sau khi chỉnh sửa xong file `{cwd}/docs/SRS_V4.md`, hãy:

1. Tóm tắt danh sách các chương/mục quan trọng mà bạn đã cập nhật, lưu vào file {cwd}/srs_v4_2_update_note.txt.
2. Liệt kê các điểm mâu thuẫn chính mà bạn tìm thấy giữa Code và Tài liệu cũ (nếu có), lưu vào file {cwd}/srs_v4_2_log.txt.
3. Xác nhận khi nào bạn đã sẵn sàng để tôi chạy lệnh `git diff` kiểm tra.
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
