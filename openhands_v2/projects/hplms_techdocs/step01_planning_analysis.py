"""
Step 01: Planning and Analysis for HP LMS BE Technical Documentation
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class PlanningAnalysisStep(BaseStep):
    """
    Step 01: Planning and Analysis
    
    Analyzes the HP LMS BE codebase structure and creates a comprehensive plan
    for generating technical documentation including Architecture, API specification,
    and Database schema documentation.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Planning and Analysis for HP LMS BE Documentation",
            step_number=1
        )
    
    def get_model(self) -> str:
        """Use Gemini Flash for planning and analysis tasks."""
        return "openai/local-gemini-2.5-pro"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert technical documentation analyst specializing in NestJS/TypeScript backend systems.

Your task is to analyze the HP LMS BE codebase and create a comprehensive plan for generating technical documentation.

IMPORTANT GUIDELINES:
- DO NOT scan files listed in .gitignore to avoid wasting tokens
- Focus on source code files, configuration files, and database schemas
- Ignore node_modules, dist, build directories, and other generated files
- Create a structured plan for documentation generation

{self.project_config.get_logging_rules()}

Focus on:
1. Analyzing the codebase structure and architecture
2. Identifying key modules, services, and controllers
3. Understanding the database schema and relationships
4. Planning documentation structure for Architecture, API specs, and Database schema
5. Creating a roadmap for documentation generation
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Analyze the HP LMS BE codebase located at: /home/dd/work/codes/HP/hp-lms-be

Your tasks:
1. **Codebase Analysis**:
   - Explore the project structure (src/, modules/, entities/, etc.)
   - Identify the main application modules and their purposes
   - Understand the technology stack (NestJS, TypeORM, etc.)
   - Check .gitignore to avoid scanning unnecessary files

2. **Architecture Planning**:
   - Map out the overall system architecture
   - Identify key components: controllers, services, entities, DTOs
   - Understand module relationships and dependencies
   - Note any design patterns used

3. **API Documentation Planning**:
   - Identify all REST endpoints from controllers
   - Understand request/response structures from DTOs
   - Note authentication and authorization mechanisms
   - Plan API specification structure

4. **Database Schema Planning**:
   - Analyze TypeORM entities and relationships
   - Understand database migrations
   - Map entity relationships and constraints
   - Plan database documentation structure

5. **Documentation Structure Planning**:
   Create a detailed plan for generating:
   - **Architecture Documentation**: System overview, module structure, design patterns
   - **API Specification**: Endpoints, request/response formats, authentication
   - **Database Schema**: Entity relationships, constraints, migrations

6. **Output Requirements**:
   - All documentation should be in Markdown format
   - Use Mermaid diagrams embedded directly in Markdown for visualizations
   - Structure suitable for Quarto processing
   - Include proper headings, code blocks, and cross-references

Create a comprehensive analysis report and documentation generation plan.
Save your findings and plan to the workspace for use by subsequent steps.

Log your actions to: {self.project_config.log_full_path}
"""


def main():
    """Run the Planning and Analysis step."""
    step = PlanningAnalysisStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()