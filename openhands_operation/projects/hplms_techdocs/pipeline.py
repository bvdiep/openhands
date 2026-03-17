"""
Pipeline Runner for HP LMS BE Technical Documentation Project
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


class HPLMSTechDocsStepRegistry(StepRegistry):
    """Registry for HP LMS BE Technical Documentation project steps."""
    
    def _register_default_steps(self):
        """Register the HP LMS BE Technical Documentation project steps."""
        try:
            print("Registering HP LMS BE Technical Documentation steps...")
            
            # Import and register step 01 - Planning and Analysis
            from step01_planning_analysis import PlanningAnalysisStep
            self.register_step(1, PlanningAnalysisStep, "Planning and Analysis")
            
            # Import and register step 02 - Architecture Documentation
            from step02_architecture_documentation import ArchitectureDocumentationStep
            self.register_step(2, ArchitectureDocumentationStep, "Architecture Documentation")
            
            # Import and register step 03 - API Specification
            from step03_api_specification import ApiSpecificationStep
            self.register_step(3, ApiSpecificationStep, "API Specification Documentation")
            
            # Import and register step 04 - Database Schema
            from step04_database_schema import DatabaseSchemaStep
            self.register_step(4, DatabaseSchemaStep, "Database Schema Documentation")
            
            # Import and register step 05 - Quality Assurance
            from step05_quality_assurance import QualityAssuranceStep
            self.register_step(5, QualityAssuranceStep, "Quality Assurance and Review")
            
            print("✅ All HP LMS BE Technical Documentation steps registered successfully!")
            
        except ImportError as e:
            print(f"⚠️  Warning: Could not import some steps: {e}")


def main():
    """Main CLI interface for HP LMS BE Technical Documentation project."""
    # Create runner with custom registry
    runner = PipelineRunner()
    runner.registry = HPLMSTechDocsStepRegistry()
    
    if len(sys.argv) < 2:
        print(f"\n📚 {project_config.project_name} - Technical Documentation Pipeline")
        print("=" * 70)
        print("🎯 Target: HP LMS BE System (/home/dd/work/codes/HP/hp-lms-be)")
        print(f"📁 Workspace: {project_config.workspace_path}")
        print("📋 Documentation Types: Architecture, API Specification, Database Schema")
        print("=" * 70)
        print("\n🚀 Usage:")
        print("  python pipeline.py list                    # Liệt kê tất cả steps")
        print("  python pipeline.py run <step_number>       # Chạy 1 step cụ thể")
        print("  python pipeline.py run <start> <end>       # Chạy từ step start đến end")
        print("  python pipeline.py run all                 # Chạy tất cả steps")
        print("\n💡 Ví dụ:")
        print("  python pipeline.py run 1                   # Chỉ chạy Planning & Analysis")
        print("  python pipeline.py run 1 3                 # Chạy Steps 1-3")
        print("  python pipeline.py run all                 # Chạy toàn bộ pipeline")
        print("\n📝 Steps Overview:")
        print("  Step 1: Planning and Analysis - Phân tích codebase và lập kế hoạch")
        print("  Step 2: Architecture Documentation - Tài liệu kiến trúc hệ thống")
        print("  Step 3: API Specification - Tài liệu API endpoints và schemas")
        print("  Step 4: Database Schema - Tài liệu cơ sở dữ liệu và entities")
        print("  Step 5: Quality Assurance - Kiểm tra chất lượng và hoàn thiện")
        print("=" * 70)
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        print(f"\n📚 {project_config.project_name} - Available Steps")
        print("=" * 70)
        runner.list_available_steps()
        print("=" * 70)
    
    elif command == "run":
        if len(sys.argv) < 3:
            print("❌ Thiếu tham số step number!")
            print("💡 Sử dụng: python pipeline.py run <step_number>")
            return
        
        if sys.argv[2].lower() == "all":
            print(f"\n🚀 Running complete HP LMS BE Technical Documentation pipeline...")
            print("=" * 70)
            runner.run_steps()
        elif len(sys.argv) == 3:
            try:
                step_num = int(sys.argv[2])
                print(f"\n🚀 Running Step {step_num} for HP LMS BE Technical Documentation...")
                print("=" * 70)
                runner.run_step(step_num)
            except ValueError:
                print("❌ Step number phải là số!")
                print("💡 Ví dụ: python pipeline.py run 1")
        elif len(sys.argv) == 4:
            try:
                start_step = int(sys.argv[2])
                end_step = int(sys.argv[3])
                print(f"\n🚀 Running Steps {start_step}-{end_step} for HP LMS BE Technical Documentation...")
                print("=" * 70)
                runner.run_steps(start_step, end_step)
            except ValueError:
                print("❌ Step numbers phải là số!")
                print("💡 Ví dụ: python pipeline.py run 1 3")
        else:
            print("❌ Quá nhiều tham số!")
            print("💡 Sử dụng: python pipeline.py run <start> <end>")
    else:
        print(f"❌ Lệnh không hợp lệ: {command}")
        print("💡 Các lệnh hợp lệ: list, run")


if __name__ == "__main__":
    main()