"""
Pipeline Runner for Cloudflare Workers Project

This pipeline orchestrates the creation of a complete Cloudflare Workers
management repository with screenshot functionality and basic authentication support.
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from engine.config import set_project_config
from project_config import project_config

# Set the project configuration before importing pipeline
set_project_config(project_config)

# Now import and use the shared pipeline
from engine.pipeline import PipelineRunner, StepRegistry


class CloudflareWorkersStepRegistry(StepRegistry):
    """Registry for Cloudflare Workers project steps."""
    
    def _register_default_steps(self):
        """Register the Cloudflare Workers project steps."""
        try:
            print("🚀 Registering Cloudflare Workers Pipeline Steps...")
            
            # Import and register step 01 - Repository Initialization
            from step01_repo_initialization import RepositoryInitializationStep
            self.register_step(1, RepositoryInitializationStep, "Repository Initialization & Setup")
            
            # Import and register step 02 - Screenshot Worker Implementation
            from step02_screenshot_worker import ScreenshotWorkerStep
            self.register_step(2, ScreenshotWorkerStep, "Screenshot Worker with Basic Auth")
            
            # Import and register step 03 - Documentation and Automation
            from step03_documentation_automation import DocumentationAutomationStep
            self.register_step(3, DocumentationAutomationStep, "Documentation & Automation Setup")
            
            print("✅ All Cloudflare Workers steps registered successfully!")
            
        except ImportError as e:
            print(f"⚠️  Warning: Could not import some steps: {e}")
            print("Make sure all step files are present in the project directory.")


def main():
    """Main CLI interface for Cloudflare Workers project."""
    # Create runner with custom registry
    runner = PipelineRunner()
    runner.registry = CloudflareWorkersStepRegistry()
    
    if len(sys.argv) < 2:
        print(f"\n🔧 {project_config.project_name.upper()} - Pipeline Runner")
        print("=" * 70)
        print("📋 Project: Cloudflare Workers Management Repository")
        print("🎯 Goal: Create screenshot worker with basic authentication")
        print(f"📁 Workspace: {project_config.workspace_path}")
        print("=" * 70)
        print("\n📖 PIPELINE OVERVIEW:")
        print("  Step 1: Repository Initialization & Setup")
        print("    • Initialize git repository")
        print("    • Create directory structure")
        print("    • Install Wrangler CLI")
        print("    • Setup TypeScript configuration")
        print()
        print("  Step 2: Screenshot Worker with Basic Auth")
        print("    • Implement screenshot worker using Browser Rendering API")
        print("    • Add basic authentication support")
        print("    • Configure wrangler.toml")
        print("    • Handle protected URLs")
        print()
        print("  Step 3: Documentation & Automation Setup")
        print("    • Create comprehensive README.md")
        print("    • Build Makefile for easy deployment")
        print("    • Add example image-optimizer worker")
        print("    • Document secret token management")
        print()
        print("=" * 70)
        print("\n🚀 USAGE:")
        print("  python pipeline.py list                    # Liệt kê tất cả steps")
        print("  python pipeline.py run <step_number>       # Chạy 1 step cụ thể")
        print("  python pipeline.py run <start> <end>       # Chạy từ step start đến end")
        print("  python pipeline.py run all                 # Chạy tất cả steps")
        print()
        print("💡 VÍ DỤ:")
        print("  python pipeline.py run 1                   # Chỉ setup repository")
        print("  python pipeline.py run 2                   # Chỉ tạo screenshot worker")
        print("  python pipeline.py run 1 2                 # Setup + Screenshot worker")
        print("  python pipeline.py run all                 # Chạy toàn bộ pipeline")
        print()
        print("📚 THAM KHẢO:")
        print("  • Cloudflare Browser Rendering: https://developers.cloudflare.com/browser-rendering/")
        print("  • Wrangler CLI: https://developers.cloudflare.com/workers/wrangler/")
        print("  • Workers Documentation: https://developers.cloudflare.com/workers/")
        print("=" * 70)
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        print("\n📋 AVAILABLE STEPS:")
        print("=" * 50)
        runner.list_available_steps()
        print("\n💡 Use 'python pipeline.py run <step_number>' to execute a specific step")
        print("💡 Use 'python pipeline.py run all' to execute the complete pipeline")
    
    elif command == "run":
        if len(sys.argv) < 3:
            print("❌ Thiếu tham số step number!")
            print("💡 Sử dụng: python pipeline.py run <step_number>")
            print("💡 Hoặc: python pipeline.py run all")
            return
        
        if sys.argv[2].lower() == "all":
            print("\n🚀 STARTING COMPLETE CLOUDFLARE WORKERS PIPELINE")
            print("=" * 60)
            print("This will create a complete Cloudflare Workers management repository")
            print("with screenshot functionality and basic authentication support.")
            print("=" * 60)
            runner.run_steps()
        elif len(sys.argv) == 3:
            try:
                step_num = int(sys.argv[2])
                print(f"\n🎯 RUNNING STEP {step_num}")
                print("=" * 40)
                runner.run_step(step_num)
            except ValueError:
                print("❌ Step number phải là số!")
                print("💡 Ví dụ: python pipeline.py run 1")
        elif len(sys.argv) == 4:
            try:
                start_step = int(sys.argv[2])
                end_step = int(sys.argv[3])
                print(f"\n🎯 RUNNING STEPS {start_step} TO {end_step}")
                print("=" * 50)
                runner.run_steps(start_step, end_step)
            except ValueError:
                print("❌ Step numbers phải là số!")
                print("💡 Ví dụ: python pipeline.py run 1 2")
        else:
            print("❌ Quá nhiều tham số!")
            print("💡 Sử dụng: python pipeline.py run <start> <end>")
    
    elif command == "info":
        print(f"\n📊 PROJECT INFORMATION")
        print("=" * 50)
        print(f"Project Name: {project_config.project_name}")
        print(f"Workspace: {project_config.workspace_path}")
        print(f"Log File: {project_config.log_full_path}")
        print("\n🎯 PROJECT GOALS:")
        print("• Create a repository for managing multiple Cloudflare Workers")
        print("• Implement a screenshot worker with basic authentication")
        print("• Use Cloudflare Browser Rendering API")
        print("• Provide comprehensive documentation and automation")
        print("\n📁 EXPECTED STRUCTURE:")
        print("cloudflare-workers/")
        print("├── screenshot-web/           # Screenshot worker")
        print("│   ├── src/index.ts")
        print("│   └── wrangler.toml")
        print("├── image-optimizer/          # Example worker")
        print("│   ├── src/index.ts")
        print("│   └── wrangler.toml")
        print("├── Makefile                  # Deployment automation")
        print("└── README.md                 # Documentation & secrets")
    
    else:
        print(f"❌ Lệnh không hợp lệ: {command}")
        print("💡 Các lệnh hợp lệ: list, run, info")
        print("💡 Sử dụng 'python pipeline.py' để xem hướng dẫn đầy đủ")


if __name__ == "__main__":
    main()