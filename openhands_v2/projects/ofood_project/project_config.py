"""
Project-specific configuration for OFood Clone project.
"""
import sys
from pathlib import Path

# Add parent directory to path to import shared config
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from config import ProjectConfig


# Create project configuration
project_config = ProjectConfig(
    project_name="ofood-clone-v1",
    target_url="https://ofood.bsmlabs.io",
    workspace_subdir="ofood-clone-v1",
    tech_stack={
        "framework": "Vite + React",
        "styling": "Tailwind CSS",
        "language": "TypeScript",
        "icons": "Lucide React"
    }
)
