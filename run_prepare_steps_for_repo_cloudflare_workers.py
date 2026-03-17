import os
from openhands_v2.runner import run_task

# 1. Cấu hình
cwd = "/home/dd/work/diep/openhands/openhands_v2/projects/cloudflare-workers"
sample_templates = "/home/dd/work/diep/openhands/openhands_v2/projects/_template"

# 2. Nhiệm vụ
task_prompt = f"""
Nhiệm vụ: Xây dựng các steps và pipeline cần thiết trong {cwd} dựa vào các steps mẫu ở {sample_templates} để cho openhands thực hiện nhiệm vụ sau: "Khởi tạo một repo dự án quản lý các workers cloudflare. Đồng thời triển khai một worker đầu tiên phục vụ cho việc chụp ảnh màn hình screenshot của một url được protected bởi basic authentication."

Chú ý là nhiệm vụ của bạn chỉ dừng lại ở việc tạo ra steps và pipeline, bạn không thực thi việc tạo repo hay triển khai worker.

Các bước thực hiện:
1. Đọc cấu hình project trong {cwd}/project_config.py
2. Tạo các steps dựa theo templates. Chú ý nêu một số tham số sau vào trong promptings.
    - Tài liệu hỗ trợ cho việc tích hợp headless browser để làm screenshot ở đây: https://developers.cloudflare.com/browser-rendering/
    - Đề xuất cấu trúc thư mục như sau:
        cloudflare-workers/
        ├── screenshot-web/           # Worker chụp ảnh màn hình
        │   ├── src/index.ts
        │   └── wrangler.toml
        ├── image-optimizer/          # (Ví dụ) Worker xử lý ảnh
        │   ├── src/index.ts
        │   └── wrangler.toml
        ├── Makefile                  # Để bạn gõ 'make deploy-screenshot' cho nhanh
        └── README.md                 # Ghi chú chung về các mã Secret Token
3. Tạo pipline trong đó ghép các steps lại.
"""

# 3. Chạy nhiệm vụ
if __name__ == "__main__":
    run_task(
        task_prompt=task_prompt,
        workspace=cwd,
        model="openai/sonnet-4",
        success_message="Nhiệm vụ hoàn tất! Kiểm tra code"
    )
