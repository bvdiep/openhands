"""
Pipeline Runner for OFood Clone Project
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from config import set_project_config
from project_config import project_config

# Set the project configuration before importing pipeline
set_project_config(project_config)

# Now import and use the shared pipeline
from pipeline import PipelineRunner, StepRegistry


class OFoodStepRegistry(StepRegistry):
    """Registry for OFood project steps."""
    
    def _register_default_steps(self):
        """Register the OFood project steps."""
        try:
            # Import and register step 01
            from ofood_step01 import PlanningStep
            self.register_step(1, PlanningStep, "Planning & Analysis")
            
            # Import and register step 02
            from ofood_step02 import PrepareCodebaseStep
            self.register_step(2, PrepareCodebaseStep, "Prepare Codebase")
            
            # Add more steps as needed...
            
        except ImportError as e:
            print(f"Warning: Could not import some steps: {e}")


def main():
    """Main CLI interface for OFood project."""
    # Create runner with custom registry
    runner = PipelineRunner()
    runner.registry = OFoodStepRegistry()
    
    if len(sys.argv) < 2:
        print(f"\n🔧 {project_config.project_name} - Pipeline Runner")
        print("=" * 60)
        print(f"Target: {project_config.target_url}")
        print(f"Workspace: {project_config.workspace_path}")
        print("=" * 60)
        print("\nUsage:")
        print("  python pipeline.py list                    # Liệt kê tất cả steps")
        print("  python pipeline.py run <step_number>       # Chạy 1 step cụ thể")
        print("  python pipeline.py run <start> <end>       # Chạy từ step start đến end")
        print("  python pipeline.py run all                 # Chạy tất cả steps")
        print("\nVí dụ:")
        print("  python pipeline.py run 1                   # Chỉ chạy Step 01")
        print("  python pipeline.py run 1 2                 # Chạy Step 01, 02")
        print("  python pipeline.py run all                 # Chạy tất cả")
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
