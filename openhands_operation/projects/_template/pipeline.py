"""
Pipeline Runner for Sample Project
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


class SampleProjectStepRegistry(StepRegistry):
    """Registry for Sample project steps."""
    
    def _register_default_steps(self):
        """Register the Sample project steps."""
        try:
            print("Theo cac cach import steps sau")
            # Import and register step 01
            # from bsmlp_step01 import InfrastructureStep
            # self.register_step(1, InfrastructureStep, "Infra preparation")
            
            # # Import and register step 02
            # from bsmlp_step02 import TailpressScaffoldingStep
            # self.register_step(2, TailpressScaffoldingStep, "Wordpress theme boiplate")
            
            # from bsmlp_step03 import TailpressPlanningStep
            # self.register_step(3, TailpressPlanningStep, "Tailpress Planning")
            
            # from bsmlp_step04 import HeaderNavigationStep
            # self.register_step(4, HeaderNavigationStep, "Header & Navigation")
            
            # from bsmlp_step05 import FixCrashStep4Step
            # self.register_step(5, FixCrashStep4Step, "Fix crash on step 4")
            
            # from bsmlp_step06 import HeroSectionStep
            # self.register_step(6, HeroSectionStep, "Implement Hero")
            
            # from bsmlp_step07 import SocialProofStep
            # self.register_step(7, SocialProofStep, "Social Proof")
            
            # from bsmlp_step08 import AppEcosystemStep
            # self.register_step(8, AppEcosystemStep, "App eco system")
            
            # from bsmlp_step09 import ProductionOptimizationStep
            # self.register_step(9, ProductionOptimizationStep, "Production Optimization")
            
        except ImportError as e:
            print(f"Warning: Could not import some steps: {e}")


def main():
    """Main CLI interface for Sample project."""
    # Create runner with custom registry
    runner = PipelineRunner()
    runner.registry = SampleProjectStepRegistry()
    
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
