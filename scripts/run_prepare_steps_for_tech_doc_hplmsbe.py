from engine.runner import run_task

# 1. Cấu hình
cwd = "/home/dd/work/diep/openhands/projects/hplms_techdocs"
sample_templates = "/home/dd/work/diep/openhands/projects/_template"
be_root = "/home/dd/work/codes/HP/hp-lms-be"

# 2. Nhiệm vụ
task_prompt = f"""
Role: Bạn là một OpenHands Pipeline Engineer chuyên nghiệp.

Nhiệm vụ: Thiết lập hệ thống Steps và Pipeline trong {cwd} để chuẩn bị cho nhiệm vụ: "Làm tài liệu kỹ thuật tự động cho hệ thống HP LMS BE". Sử dụng các mẫu tại {sample_templates} làm chuẩn.

Yêu cầu nghiêm ngặt: Bạn CHỈ tạo ra file cấu hình và code điều khiển (meta-coding), KHÔNG trực tiếp thực thi các tác vụ scan code hay viết tài liệu.

Các bước thực hiện:
1. Tạo ra file {cwd}/project_config.py dựa theo mẫu trong {sample_templates}/project_config.py. Trong file này, bạn cần các trường bắt buộc gồm project_name (hãy lấy hplmsbe_techdoc) và workspace_subdir (cũng hãy lấy hplmsbe_techdoc). Vì chúng ta chuẩn bị review nên techstack sẽ chưa có.
2. Tạo các steps dựa theo templates. Chú ý đến một số tham số sau.
    - Thư mục của project BE cần làm tài liệu kỹ thuật là {be_root}, điều này quan trọng cần đưa vào prompting.
    - Tạo ra các steps theo mẫu ExampleStepWithGPT4() ở trong {sample_templates}/step_example_custom_model.py. Hãy sử dụng openai/local-gemini-3-flash là model mà tôi có ở litellm proxy cho tất cả các steps.
    - Các prompts cần chú ý nhắc nhở không scan các files ở .gitignore để tránh lãng phí token.
    - Tài liệu cần có 3 loại: Architect, Api specification và Database schema
    - Tài liệu cần có định dạng markdown
    - Các hình vẽ sử dụng mermaid nhúng trực tiếp trong tài liệu markdown để tôi có thể xử lý view được bằng quarto.
    - Cần chú ý bước lập kế hoạch trước khi thực hiện để đảm bảo độ chính xác.
    - Cần bước kiểm tra nữa.
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
