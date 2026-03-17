"""
Project-specific configuration for HP LMS BE Technical Documentation.
"""
import sys
from pathlib import Path

# Add parent directory to path to import shared config
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from config import ProjectConfig


# Create project configuration
project_config = ProjectConfig(
    project_name="hplmsbe_techdoc",  # REQUIRED: Unique project name
    workspace_subdir="hplmsbe_techdoc",  # REQUIRED: Workspace subdirectory name
    # tech_stack will be determined during analysis phase
)