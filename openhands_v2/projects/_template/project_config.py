"""
Project-specific configuration template.
Copy this file and customize for your project.
"""
import sys
from pathlib import Path

# Add parent directory to path to import shared config
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from config import ProjectConfig


# Create project configuration
project_config = ProjectConfig(
    project_name="your-project-name",  # REQUIRED: Unique project name
    target_url="https://example.com",  # Optional: Target URL if cloning a website
    workspace_subdir="your-project-name",  # Optional: Workspace subdirectory name
    tech_stack={  # Optional: Customize your tech stack
        "framework": "Vite + React",
        "styling": "Tailwind CSS",
        "language": "TypeScript",
        "icons": "Lucide React"
    }
)
