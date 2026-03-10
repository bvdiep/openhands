"""
Step 01: Planning Phase
Analyze target website and create implementation plan.
"""
from base_step import BaseStep


class PlanningStep(BaseStep):
    """Step 01: Analyze website and create detailed plan."""
    
    def __init__(self):
        super().__init__(
            step_name="Planning & Analysis",
            step_number=1
        )
    
    def get_system_prompt(self) -> str:
        return f"""
Bạn là một Technical Architect và Senior Full-stack Engineer.
Nhiệm vụ của bạn là phân tích và tái tạo (clone) trang web mục tiêu với độ chính xác cao nhất.

{self.project_config.get_logging_rules()}

QUY TRÌNH THỰC HIỆN:
- Bước 1: Khám phá. Sử dụng trình duyệt để soi chi tiết trang web.
- Bước 2: Ghi chép. Đóng gói kiến thức vào tài liệu trước khi viết code.
- Bước 3: Thực thi. Code đến đâu, kiểm tra (verify) đến đó.

Mọi lệnh chạy và file tạo ra phải hướng tới mục tiêu cuối cùng:
Một bản clone SPA hoàn hảo bằng Vite + React + Tailwind.
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Mục tiêu: Phân tích và lập kế hoạch tái tạo trang web tại URL: {self.project_config.target_url}

Nhiệm vụ của bạn:
1. Khởi tạo ngay file '{self.project_config.project_log_filename}' và ghi lại bước đầu tiên:
   "Bắt đầu phân tích dự án {self.project_config.target_url}".
2. Sử dụng trình duyệt để phân tích trang web (Layout, màu sắc, font, components).
3. Cập nhật mọi phát hiện quan trọng vào '{self.project_config.project_log_filename}' theo quy tắc Traceability.
4. Viết bản kế hoạch chi tiết vào file '{self.project_config.plan_filename}'.

Yêu cầu bản kế hoạch:
- Techstack: Vite + React + Tailwind CSS.
- Phân tích các sections chính của trang {self.project_config.target_url}.
- Liệt kê các thư viện cần cài đặt thêm.
- Các bước triển khai code cụ thể cho giai đoạn tiếp theo.

Sau khi ghi file '{self.project_config.plan_filename}' và hoàn tất nhật ký trong '{self.project_config.project_log_filename}',
hãy xác nhận với tôi.
"""


def main():
    """Run Step 01: Planning Phase."""
    step = PlanningStep()
    success = step.run()
    
    if success:
        print("\n✓ Step 01 hoàn tất. Có thể chạy Step 02.")
    else:
        print("\n✗ Step 01 thất bại. Vui lòng kiểm tra lỗi.")
    
    return success


if __name__ == "__main__":
    main()
