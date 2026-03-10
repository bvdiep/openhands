# OpenHands Pipeline Framework - Multi-Project Support

Hệ thống pipeline được refactor để hỗ trợ nhiều dự án, mỗi dự án có conversation ID riêng và workspace riêng.

## 🏗️ Cấu trúc mới

```
openhands_v2/
├── config.py                    # Cấu hình chung (LLM, ProjectConfig class)
├── base_step.py                 # Base class cho tất cả steps
├── pipeline.py                  # Shared pipeline runner
├── projects/                    # Thư mục chứa các dự án
│   ├── ofood_project/          # Ví dụ: Dự án OFood Clone
│   │   ├── project_config.py   # Cấu hình riêng của dự án
│   │   ├── pipeline.py         # Pipeline runner cho dự án này
│   │   ├── step_01_planning.py # Step 01 của dự án
│   │   ├── step_02_prepare_codebase.py
│   │   └── ...                 # Các steps khác
│   └── your_project/           # Dự án mới của bạn
│       ├── project_config.py
│       ├── pipeline.py
│       └── step_*.py
├── workspace/                   # Workspace cho tất cả dự án
│   ├── ofood-clone-v1/         # Workspace riêng cho từng dự án
│   └── your-project/
└── .conversations/              # Lưu trữ conversation state (theo conversation_id)
```

## 🚀 Cách sử dụng

### Chạy dự án có sẵn (OFood)

```bash
cd projects/ofood_project/

# Liệt kê tất cả steps
python pipeline.py list

# Chạy 1 step cụ thể
python pipeline.py run 1

# Chạy từ step 1 đến step 2
python pipeline.py run 1 2

# Chạy tất cả steps
python pipeline.py run all
```

### Tạo dự án mới

#### Bước 1: Tạo thư mục dự án

```bash
mkdir -p projects/your_project
cd projects/your_project
```

#### Bước 2: Tạo file cấu hình dự án

Tạo file `project_config.py`:

```python
"""
Project-specific configuration for Your Project.
"""
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from config import ProjectConfig

# Create project configuration
project_config = ProjectConfig(
    project_name="your-project-v1",
    target_url="https://example.com",  # Optional
    workspace_subdir="your-project-v1",  # Optional, defaults to project_name
    tech_stack={
        "framework": "Vite + React",
        "styling": "Tailwind CSS",
        "language": "TypeScript",
        "icons": "Lucide React"
    }
)
```

#### Bước 3: Tạo pipeline runner

Tạo file `pipeline.py`:

```python
"""
Pipeline Runner for Your Project
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from config import set_project_config
from project_config import project_config

# Set the project configuration
set_project_config(project_config)

# Import shared pipeline
from pipeline import PipelineRunner, StepRegistry


class YourProjectStepRegistry(StepRegistry):
    """Registry for your project steps."""
    
    def _register_default_steps(self):
        """Register your project steps."""
        try:
            from step_01_your_step import YourStep
            self.register_step(1, YourStep, "Your Step Name")
            
            # Add more steps...
            
        except ImportError as e:
            print(f"Warning: Could not import some steps: {e}")


def main():
    """Main CLI interface."""
    runner = PipelineRunner()
    runner.registry = YourProjectStepRegistry()
    
    if len(sys.argv) < 2:
        print(f"\n🔧 {project_config.project_name} - Pipeline Runner")
        print("=" * 60)
        print(f"Workspace: {project_config.workspace_path}")
        print("=" * 60)
        print("\nUsage:")
        print("  python pipeline.py list")
        print("  python pipeline.py run <step_number>")
        print("  python pipeline.py run <start> <end>")
        print("  python pipeline.py run all")
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        runner.list_available_steps()
    elif command == "run":
        if len(sys.argv) < 3:
            print("❌ Thiếu tham số step number!")
            return
        
        if sys.argv[2].lower() == "all":
            runner.run_steps()
        elif len(sys.argv) == 3:
            try:
                step_num = int(sys.argv[2])
                runner.run_step(step_num)
            except ValueError:
                print("❌ Step number phải là số!")
        elif len(sys.argv) == 4:
            try:
                start_step = int(sys.argv[2])
                end_step = int(sys.argv[3])
                runner.run_steps(start_step, end_step)
            except ValueError:
                print("❌ Step numbers phải là số!")
        else:
            print("❌ Quá nhiều tham số!")
    else:
        print(f"❌ Lệnh không hợp lệ: {command}")


if __name__ == "__main__":
    main()
```

#### Bước 4: Tạo steps

Tạo file `step_01_your_step.py`:

```python
"""
Step 01: Your Step Description
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class YourStep(BaseStep):
    """Step 01: Your step description."""
    
    def __init__(self):
        super().__init__(
            step_name="Your Step Name",
            step_number=1
        )
    
    def get_system_prompt(self) -> str:
        return f"""
Your system prompt here...

{self.project_config.get_logging_rules()}

Additional instructions...
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Your user prompt here...

Target: {self.project_config.target_url}
Workspace: {self.project_config.workspace_path}
"""


def main():
    """Run Step 01."""
    step = YourStep()
    success = step.run()
    
    if success:
        print("\n✓ Step 01 hoàn tất.")
    else:
        print("\n✗ Step 01 thất bại.")
    
    return success


if __name__ == "__main__":
    main()
```

## ✨ Ưu điểm của cấu trúc mới

### 1. **Multi-Project Support**
- Mỗi dự án có conversation ID riêng
- Workspace riêng cho từng dự án
- Không bị xung đột giữa các dự án

### 2. **Shared Core Components**
- [`config.py`](config.py): Cấu hình LLM và ProjectConfig class dùng chung
- [`base_step.py`](base_step.py): Base class cho tất cả steps
- [`pipeline.py`](pipeline.py): Pipeline runner dùng chung

### 3. **Project-Specific Components**
- `project_config.py`: Cấu hình riêng (tên dự án, URL, tech stack)
- `pipeline.py`: Pipeline runner với steps đăng ký riêng
- `step_*.py`: Các steps riêng cho từng dự án

### 4. **Easy Project Management**
- Tạo dự án mới chỉ cần copy template
- Mỗi dự án độc lập, không ảnh hưởng lẫn nhau
- Dễ dàng quản lý nhiều dự án song song

## 📝 ProjectConfig API

```python
class ProjectConfig:
    def __init__(
        self,
        project_name: str,              # Tên dự án (unique)
        target_url: Optional[str],      # URL mục tiêu (nếu có)
        workspace_subdir: Optional[str], # Tên thư mục workspace
        tech_stack: Optional[Dict]      # Tech stack configuration
    )
    
    # Properties
    .project_name           # Tên dự án
    .target_url            # URL mục tiêu
    .conversation_id       # UUID duy nhất cho dự án
    .workspace_path        # Đường dẫn workspace
    .persistence_dir       # Thư mục lưu conversation state
    .plan_full_path        # Đường dẫn file plan
    .log_full_path         # Đường dẫn file log
    .tech_stack            # Tech stack configuration
    
    # Methods
    .get_logging_rules()   # Lấy quy tắc logging
```

## 🎯 Lợi ích

1. **Reusability**: Core components được tái sử dụng cho nhiều dự án
2. **Isolation**: Mỗi dự án độc lập, không ảnh hưởng lẫn nhau
3. **Maintainability**: Dễ bảo trì và cập nhật
4. **Scalability**: Dễ dàng thêm dự án mới
5. **Consistency**: Tất cả dự án follow cùng 1 pattern
6. **Flexibility**: Mỗi dự án có thể customize theo nhu cầu

## 📂 Workspace Organization

```
workspace/
├── ofood-clone-v1/          # Dự án 1
│   ├── PROJECT_PLAN.md
│   ├── PROJECT_LOG.md
│   ├── .metadata/
│   └── [generated code]
├── your-project-v1/         # Dự án 2
│   ├── PROJECT_PLAN.md
│   ├── PROJECT_LOG.md
│   └── ...
└── another-project/         # Dự án 3
    └── ...
```

## 🔄 Migration từ cấu trúc cũ

Nếu bạn có dự án cũ, chỉ cần:

1. Tạo thư mục mới trong `projects/`
2. Copy các step files vào
3. Tạo `project_config.py` và `pipeline.py`
4. Update imports trong các step files
5. Chạy pipeline mới

## 💡 Tips

- Sử dụng tên dự án có ý nghĩa và unique
- Mỗi dự án nên có workspace_subdir riêng
- Conversation state được lưu tự động theo conversation_id
- Có thể chạy nhiều dự án song song mà không bị conflict
