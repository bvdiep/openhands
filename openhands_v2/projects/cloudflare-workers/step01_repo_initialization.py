"""
Step 01: Repository Initialization for Cloudflare Workers Project

This step initializes the repository structure and sets up the basic environment
for managing multiple Cloudflare Workers.
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class RepositoryInitializationStep(BaseStep):
    """
    Step 01: Initialize repository and basic structure for Cloudflare Workers project.
    
    This step will:
    1. Initialize git repository
    2. Create the recommended directory structure
    3. Install and configure Wrangler CLI
    4. Set up basic project configuration
    """
    
    def __init__(self):
        super().__init__(
            step_name="Repository Initialization",
            step_number=1
        )
    
    # def get_model(self) -> str:
    #     return "openai/kimi-2.5"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert Cloudflare Workers developer tasked with initializing a new repository for managing multiple Cloudflare Workers.

IMPORTANT DOCUMENTATION:
- Cloudflare Browser Rendering API: https://developers.cloudflare.com/browser-rendering/
- Wrangler CLI Documentation: https://developers.cloudflare.com/workers/wrangler/

REQUIRED DIRECTORY STRUCTURE:
Create the following structure in the workspace:
```
cloudflare-workers/
├── screenshot-web/           # Worker chụp ảnh màn hình
│   ├── src/index.ts
│   └── wrangler.toml
├── image-optimizer/          # (Ví dụ) Worker xử lý ảnh
│   ├── src/index.ts
│   └── wrangler.toml
├── Makefile                  # Để bạn gõ 'make deploy-screenshot' cho nhanh
└── README.md                 # Ghi chú chung về các mã Secret Token
```

TASKS FOR THIS STEP:
1. Initialize git repository if not already initialized
2. Create the directory structure above
3. Install Wrangler CLI globally (npm install -g wrangler)
4. Create basic package.json for the project
5. Create .gitignore file appropriate for Node.js/TypeScript projects
6. Create basic TypeScript configuration (tsconfig.json)
7. Verify Wrangler installation and show version

IMPORTANT NOTES:
- Use TypeScript for all workers
- Ensure proper git configuration
- Create placeholder files where needed
- Don't deploy anything yet - this is just setup

{self.project_config.get_logging_rules()}
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Initialize a new Cloudflare Workers repository with the following requirements:

PROJECT DETAILS:
- Project Name: {self.project_config.project_name}
- Workspace: {self.project_config.workspace_path}
- Purpose: Manage multiple Cloudflare Workers, starting with a screenshot service

STEP 1 TASKS:
1. **Repository Setup**:
   - Initialize git repository in the workspace
   - Create appropriate .gitignore for Node.js/TypeScript
   - Set up initial commit

2. **Directory Structure**:
   Create the exact structure:
   ```
   cloudflare-workers/
   ├── screenshot-web/
   │   ├── src/
   │   └── (wrangler.toml will be created in next step)
   ├── image-optimizer/
   │   ├── src/
   │   └── (wrangler.toml will be created later)
   ├── (Makefile will be created in step 3)
   └── (README.md will be created in step 3)
   ```

3. **Development Environment**:
   - Create package.json with basic dependencies
   - Install Wrangler CLI: `npm install -g wrangler`
   - Create tsconfig.json for TypeScript support
   - Verify Wrangler installation with `wrangler --version`

4. **Initial Files**:
   - Create placeholder index.ts files in both worker directories
   - Add basic TypeScript interfaces/types if needed
   - Ensure all directories are properly created

VERIFICATION:
- Confirm git repository is initialized
- Verify directory structure matches requirements
- Check Wrangler CLI is installed and working
- Ensure TypeScript configuration is valid

Log all actions to: {self.project_config.log_full_path}

Do NOT create wrangler.toml files yet - those will be handled in the next step.
Do NOT deploy anything - this is setup only.
"""


def main():
    """Run the Repository Initialization step."""
    step = RepositoryInitializationStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()