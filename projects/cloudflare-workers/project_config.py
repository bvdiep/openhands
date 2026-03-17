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
    project_name="cloudflare-workers",  # REQUIRED: Unique project name
    workspace_subdir="cloudflare-workers",
    tech_stack={  # Technology stack for this project
        "platform": "Cloudflare Workers",
        "language": "TypeScript",
        "runtime": "Workers Runtime",
        "tools": "Wrangler CLI",
        "apis": "Browser Rendering API"
    }
)
