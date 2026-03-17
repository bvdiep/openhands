"""
Step 03: Documentation and Automation Setup

This step creates the Makefile for easy deployment commands and comprehensive
documentation including README with secret token management instructions.
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class DocumentationAutomationStep(BaseStep):
    """
    Step 03: Create documentation, automation tools, and example worker.
    
    This step will:
    1. Create Makefile with deployment commands
    2. Create comprehensive README.md
    3. Create example image-optimizer worker
    4. Set up development and deployment workflows
    """
    
    def __init__(self):
        super().__init__(
            step_name="Documentation and Automation Setup",
            step_number=3
        )
    
    # def get_model(self) -> str:
    #     return "openai/kimi-2.5"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert DevOps engineer and technical writer specializing in Cloudflare Workers deployment and documentation.

DOCUMENTATION REQUIREMENTS:
Create comprehensive documentation that covers:
1. **Project Overview**: Purpose and architecture
2. **Setup Instructions**: Environment setup and prerequisites
3. **Secret Management**: Cloudflare API tokens, environment variables
4. **Deployment Guide**: Step-by-step deployment instructions
5. **Usage Examples**: API usage with curl examples
6. **Development Workflow**: Local development and testing
7. **Troubleshooting**: Common issues and solutions

AUTOMATION REQUIREMENTS:
Create a Makefile with the following targets:
- `make install`: Install dependencies and setup
- `make deploy-screenshot`: Deploy screenshot worker
- `make deploy-optimizer`: Deploy image optimizer worker
- `make deploy-all`: Deploy all workers
- `make dev-screenshot`: Start local development for screenshot worker
- `make dev-optimizer`: Start local development for image optimizer
- `make logs-screenshot`: View screenshot worker logs
- `make logs-optimizer`: View image optimizer logs
- `make clean`: Clean build artifacts
- `make help`: Show available commands

EXAMPLE WORKER REQUIREMENTS:
Create a second worker (image-optimizer) to demonstrate:
- Multi-worker project structure
- Different worker functionality
- Shared configuration patterns
- Deployment automation

SECURITY FOCUS:
Emphasize proper secret management:
- Cloudflare API tokens
- Environment variables
- Wrangler authentication
- Production vs development configurations

{self.project_config.get_logging_rules()}
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Create comprehensive documentation and automation tools for the Cloudflare Workers project.

PROJECT CONTEXT:
- Project: {self.project_config.project_name}
- Workspace: {self.project_config.workspace_path}
- Current Structure: screenshot-web/ and image-optimizer/ directories exist

STEP 3 DELIVERABLES:

1. **Create Makefile**:
   Create a comprehensive Makefile with these targets:
   
   ```makefile
   # Installation and setup
   install: Install wrangler and dependencies
   setup: Initial project setup and authentication
   
   # Development
   dev-screenshot: Start local dev server for screenshot worker
   dev-optimizer: Start local dev server for image optimizer
   
   # Deployment
   deploy-screenshot: Deploy screenshot worker to Cloudflare
   deploy-optimizer: Deploy image optimizer worker
   deploy-all: Deploy all workers
   
   # Monitoring
   logs-screenshot: Tail logs for screenshot worker
   logs-optimizer: Tail logs for image optimizer
   
   # Utilities
   clean: Clean build artifacts and temporary files
   help: Show this help message
   ```

2. **Create README.md**:
   Write comprehensive documentation including:
   
   **Sections Required**:
   - Project overview and architecture
   - Prerequisites and setup instructions
   - **Secret Token Management** (detailed section)
   - Worker descriptions and APIs
   - Deployment instructions
   - Usage examples with curl commands
   - Development workflow
   - Troubleshooting guide
   
   **Secret Management Section Must Include**:
   - How to get Cloudflare API token
   - Wrangler authentication setup
   - Environment variables configuration
   - Security best practices
   - Production vs development configs

3. **Create image-optimizer worker**:
   Implement a second worker in `image-optimizer/` with:
   
   **Features**:
   - Image resizing and optimization
   - Format conversion (PNG, JPEG, WebP)
   - Quality adjustment
   - Basic image processing
   
   **Files to Create**:
   - `image-optimizer/src/index.ts`: Worker implementation
   - `image-optimizer/wrangler.toml`: Configuration
   
   **API Design**:
   - GET /optimize?url=<IMAGE_URL>&width=<W>&height=<H>&format=<FORMAT>
   - POST /optimize with JSON body for batch processing
   - Support for quality, format, and dimension parameters

4. **Development Workflow Files**:
   - `.env.example`: Template for environment variables
   - `package.json`: Update with scripts for both workers
   - Development scripts and helpers

SPECIFIC REQUIREMENTS:

**Makefile Implementation**:
- Use proper Make syntax with .PHONY targets
- Include help text for each target
- Handle errors gracefully
- Support both workers with consistent commands
- Include color output for better UX

**README Structure**:
```markdown
# Cloudflare Workers Management

## Overview
[Project description and architecture]

## Prerequisites
[Required tools and accounts]

## Secret Token Management ⚠️
[Detailed instructions for API tokens and security]

## Quick Start
[Step-by-step setup]

## Workers

### Screenshot Web Worker
[API documentation and examples]

### Image Optimizer Worker
[API documentation and examples]

## Deployment
[Deployment instructions using Makefile]

## Development
[Local development workflow]

## Troubleshooting
[Common issues and solutions]
```

**Image Optimizer Features**:
- Resize images to specified dimensions
- Convert between formats (PNG, JPEG, WebP)
- Adjust quality for lossy formats
- Maintain aspect ratio options
- Error handling for invalid images
- CORS support for web usage

EXAMPLE USAGE DOCUMENTATION:
Include practical examples like:
```bash
# Screenshot with auth
curl "https://screenshot.your-domain.workers.dev/screenshot?url=https://protected.site.com&username=user&password=pass"

# Image optimization
curl "https://optimizer.your-domain.workers.dev/optimize?url=https://example.com/image.jpg&width=800&height=600&format=webp"

# Deploy screenshot worker
make deploy-screenshot

# View logs
make logs-screenshot
```

SECURITY EMPHASIS:
- Never commit API tokens to git
- Use environment variables for secrets
- Provide clear instructions for token management
- Include security best practices section

Log all documentation creation to: {self.project_config.log_full_path}

Create production-ready documentation that a new developer could follow to set up and deploy the entire project.
"""


def main():
    """Run the Documentation and Automation Setup step."""
    step = DocumentationAutomationStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()