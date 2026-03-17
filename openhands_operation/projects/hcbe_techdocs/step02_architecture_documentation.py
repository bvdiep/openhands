"""
Step 02: Architecture Documentation for Healthcare BE
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class ArchitectureDocumentationStep(BaseStep):
    """
    Step 02: Architecture Documentation
    
    Generates comprehensive architecture documentation for the Healthcare BE system
    including system overview, module structure, design patterns, and architectural diagrams.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Architecture Documentation for Healthcare BE",
            step_number=2
        )
    
    def get_model(self) -> str:
        """Use Gemini Flash for architecture documentation tasks."""
        return "gemini/gemini-3-flash-preview"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert software architect and technical writer specializing in backend system documentation.

Your task is to create comprehensive architecture documentation for the Healthcare BE system based on the analysis from Step 01.

IMPORTANT GUIDELINES:
- DO NOT scan files listed in .gitignore to avoid wasting tokens
- Use the analysis and plan from Step 01 as your foundation
- Focus on architectural patterns, system design, and module relationships
- Create clear, professional documentation suitable for developers and stakeholders

{self.project_config.get_logging_rules()}

Focus on:
1. System architecture overview and high-level design
2. Module structure and component relationships
3. Design patterns and architectural decisions
4. Data flow and system interactions
5. Creating clear Mermaid diagrams for visualization
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Based on the analysis from Step 01, create comprehensive architecture documentation for the Healthcare BE system located at: /home/dd/work/codes/HEALTHCARE/healthcare-api

Your tasks:
1. **System Architecture Overview**:
   - Create a high-level system architecture description
   - Explain the overall system design and approach
   - Document key architectural decisions and rationale
   - Include system boundaries and external dependencies

2. **Module Structure Documentation**:
   - Document all major modules and their responsibilities
   - Explain module relationships and dependencies
   - Create module hierarchy and organization structure
   - Document inter-module communication patterns

3. **Design Patterns and Principles**:
   - Identify and document design patterns used
   - Explain architectural principles followed
   - Document coding standards and conventions
   - Note any framework-specific patterns

4. **Component Architecture**:
   - Document key components (controllers, services, repositories, etc.)
   - Explain component responsibilities and interactions
   - Create component relationship diagrams
   - Document data flow between components

5. **Mermaid Diagrams**:
   Create embedded Mermaid diagrams for:
   - System architecture overview
   - Module dependency graph
   - Component relationship diagram
   - Data flow diagram

6. **Output Requirements**:
   - Create a comprehensive Markdown document named "01_Architecture.md"
   - Use proper Markdown formatting with clear headings
   - Embed Mermaid diagrams directly in the Markdown
   - Structure suitable for Quarto processing
   - Include table of contents and cross-references

7. **Documentation Structure**:
   ```
   # Healthcare BE - System Architecture
   
   ## Table of Contents
   ## 1. System Overview
   ## 2. Architecture Principles
   ## 3. Module Structure
   ## 4. Component Architecture
   ## 5. Design Patterns
   ## 6. Data Flow
   ## 7. External Dependencies
   ## 8. Architectural Decisions
   ```

Save the architecture documentation to the workspace as "01_Architecture.md".

Log your actions to: {self.project_config.log_full_path}
"""


def main():
    """Run the Architecture Documentation step."""
    step = ArchitectureDocumentationStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()