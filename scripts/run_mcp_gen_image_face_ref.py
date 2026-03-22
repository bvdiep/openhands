# Note: mcp này đã nâng cấp cho thêm cả veo3 vào rồi, và các tham số cũng linh động hơn
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runner import run_task

# 1. Cấu hình
cwd = os.path.join(os.getcwd(), "..", "apps", "mcp_gen_img_face_ref")

# 2. Nhiệm vụ
task_prompt = f"""
Hãy giúp tôi triển khai một **MCP Server bằng Python** và thực hiện kiểm thử hoàn chỉnh.

### 1. Môi trường và Dữ liệu đầu vào:

Tôi đã chuẩn bị sẵn các tệp sau trong thư mục gốc của dự án tại {cwd}:

- File `.env` chứa `GOOGLE_API_KEY`.
- Một ảnh reference tại đường dẫn `./hv01.png`.

### 2. Yêu cầu Triển khai (Coding):

- **Cấu trúc:** Sử dụng thư viện `mcp[cli]` với chuẩn `FastMCP` để tối ưu code, đảm bảo server có thể chạy được qua cả `python` và `mcp dev`.
- **dependencies:** Tạo file `pyproject.toml` và `.env.example`. Cần dùng `python-dotenv` để đọc API key và thư viện Google GenAI SDK (hoặc `httpx` nếu gọi API trực tiếp).
- **Tool:** Tạo một công cụ tên là `generate_image_with_face`.
  - **Input:** `prompt` (string), `face_reference_path` (string, mặc định là `./hv01.png`).
  - **Model cần phải sử dụng**: gemini-3.1-flash-image-preview (google banana 2)
  - **Logic:**
    - Đọc file ảnh từ `face_reference_path`.
    - Gọi model sinh ảnh của Google (sử dụng khả năng Image-to-Image để giữ khuôn mặt từ ảnh reference).
    - Prompt cần mô tả bối cảnh mới, nhưng khuôn mặt phải giống ảnh reference.
    - **Đầu ra (Output):** Lưu ảnh được sinh ra vào thư mục `./outputs/` (tạo thư mục nếu chưa có) và trả về đường dẫn của ảnh mới.
  - **Xử lý lỗi:** Code cần xử lý các trường hợp file không tồn tại, lỗi API, hoặc API không trả về ảnh.

### 3. Yêu cầu Kiểm thử (Testing):

Sau khi viết code xong, hãy thực hiện các bước kiểm thử sau và xác nhận kết quả:

1. **Kiểm thử Unit (trong terminal):**
   - Chạy trực tiếp file python hoặc dùng `mcp dev` để gọi tool.
   - Sử dụng `face_reference_path` là `./hv01.png` và prompt: *"Cô gái việt nam xinh đẹp trong bộ ảnh váy cưới đứng ở cánh đồng hoa với khung cảnh lãng mạn"*
   - Xác nhận xem ảnh đầu ra có được tạo trong `./outputs/` hay không.
2. **Xác nhận kết quả:** Bạn (OpenHands) cần kiểm tra tệp đầu ra để đảm bảo nó không bị lỗi và thực sự chứa hình ảnh (có thể xác nhận kích thước tệp hoặc định dạng tệp).

Hãy bắt đầu bằng cách liệt kê các bước bạn sẽ thực hiện, sau đó viết code và cuối cùng là thực hiện các bài test.
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
