"""
Step 02: Architecture Documentation Generation for HP LMS BE
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class ArchitectureDocumentationStep(BaseStep):
    """
    Step 02: Architecture Documentation Generation
    
    Generates comprehensive architecture documentation for the HP LMS BE system
    including system overview, module structure, design patterns, and architectural diagrams.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Architecture Documentation Generation",
            step_number=2
        )
    
    def get_model(self) -> str:
        """Use Gemini Flash for documentation generation."""
        return "openai/local-gemini-2.5-pro"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert technical writer specializing in software architecture documentation for NestJS/TypeScript systems.

Your task is to generate comprehensive architecture documentation for the HP LMS BE system.

IMPORTANT GUIDELINES:
- DO NOT scan files listed in .gitignore to avoid wasting tokens
- Focus on architectural patterns, module structure, and system design
- Use Mermaid diagrams embedded directly in Markdown for all visualizations
- Create documentation suitable for Quarto processing
- Follow proper Markdown formatting with clear headings and structure

{self.project_config.get_logging_rules()}

Focus on:
1. System architecture overview with Mermaid diagrams
2. Module structure and dependencies
3. Design patterns and architectural decisions
4. Data flow and component interactions
5. Security architecture and authentication flow
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Generate comprehensive architecture documentation for the HP LMS BE system located at: /home/dd/work/codes/HP/hp-lms-be

Use the analysis from Step 01 as your foundation and create detailed architecture documentation.

Your tasks:
1. **System Architecture Overview**:
   - Create a high-level system architecture diagram using Mermaid
   - Describe the overall system design and architectural principles
   - Explain the technology stack and framework choices

2. **Module Architecture**:
   - Document all NestJS modules and their responsibilities
   - Create module dependency diagrams using Mermaid
   - Explain inter-module communication patterns

3. **Component Architecture**:
   - Document controllers, services, and their relationships
   - Show component interaction patterns
   - Explain dependency injection and service layer design

4. **Data Architecture**:
   - Document entity relationships and data models
   - Show database interaction patterns
   - Explain repository and service patterns

5. **Security Architecture**:
   - Document authentication and authorization mechanisms
   - Show security flow diagrams using Mermaid
   - Explain JWT handling and user management

6. **Design Patterns**:
   - Identify and document design patterns used
   - Explain architectural decisions and trade-offs
   - Document coding standards and conventions

**Output Requirements**:
- Create a single comprehensive Markdown file: `architecture-documentation.md`
- Use proper Markdown structure with clear headings
- Embed all diagrams as Mermaid code blocks directly in the Markdown
- Include code examples where relevant
- Structure suitable for Quarto processing
- Save to the workspace directory

**Mermaid Diagram Types to Use**:
- System architecture: `graph TD` or `flowchart TD`
- Module dependencies: `graph LR`
- Component relationships: `classDiagram`
- Data flow: `sequenceDiagram`
- Security flow: `sequenceDiagram`

Log your actions to: {self.project_config.log_full_path}
"""


def main():
    """Run the Architecture Documentation step."""
    step = ArchitectureDocumentationStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()