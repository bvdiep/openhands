"""
Step 02: Prepare Codebase
Initialize project structure and install dependencies.
"""
from base_step import BaseStep


class PrepareCodebaseStep(BaseStep):
    """Step 02: Setup project structure and dependencies."""
    
    def __init__(self):
        super().__init__(
            step_name="Prepare Codebase",
            step_number=2
        )
    
    def get_system_prompt(self) -> str:
        return f"""
Bạn là một Senior Frontend Developer thực thi dự án dựa trên bản thiết kế có sẵn.

{self.project_config.get_logging_rules()}

QUY TẮC GHI NHẬT KÝ VÀ TRUY XUẤT (BẮT BUỘC):
1. ĐỌC TRƯỚC: Trước khi gõ bất kỳ lệnh nào, bạn PHẢI đọc '{self.project_config.plan_full_path}'
   và '{self.project_config.log_full_path}' để nắm bắt bối cảnh.
2. GHI TIẾP: Bạn PHẢI tiếp tục ghi nhật ký vào file '{self.project_config.log_full_path}'.
   Mỗi khi cài đặt một library, tạo một component mới, hoặc sửa một lỗi,
   bạn phải ghi một dòng log mới.
3. CẤU TRÚC LOG STEP 02:
   - [Execution]: Mô tả lệnh terminal vừa chạy hoặc file vừa code.
   - [Verification]: Cách bạn kiểm tra xem bước đó có chạy đúng không.
   - [Deviation]: Nếu bạn phải làm khác đi so với Plan (do lỗi library hoặc môi trường),
     bạn phải giải trình rõ lý do tại sao.

QUY TẮC THỰC THI:
- Luôn ưu tiên Tech Stack và định hướng trong '{self.project_config.plan_full_path}'.
- Sử dụng chính xác mã màu/font từ '{self.project_config.style_guide_filename}'.
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Dựa trên kế hoạch và nghiên cứu ở Step 01:

1. Đọc và Phân tích: Đọc kỹ Plan và Log từ Step 01.
2. Ghi nhật ký: Ghi vào '{self.project_config.log_full_path}' xác nhận bạn đã sẵn sàng
   và liệt kê 3 công việc đầu tiên.
3. THỰC THI NGAY (Action): Bắt đầu chạy các lệnh Terminal để khởi tạo dự án
   theo tech stacks được đề xuất và cài đặt các thư viện theo đúng Plan.
   Không dừng lại ở việc liệt kê, hãy thực hiện cho đến khi hoàn thành xong
   cấu trúc thư mục cơ bản của dự án.
4. Báo cáo: Sau khi xong, cập nhật kết quả vào {self.project_config.log_full_path} và cho tôi biết
   bạn đã sẵn sàng để code component đầu tiên chưa.
"""


def main():
    """Run Step 02: Prepare Codebase."""
    step = PrepareCodebaseStep()
    success = step.run()
    
    if success:
        print("\n✓ Step 02 hoàn tất. Có thể chạy Step 03.")
    else:
        print("\n✗ Step 02 thất bại. Vui lòng kiểm tra lỗi.")
    
    return success


if __name__ == "__main__":
    main()
