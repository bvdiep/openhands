"""
Step 03: API Specification Documentation Generation for HP LMS BE
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class ApiSpecificationStep(BaseStep):
    """
    Step 03: API Specification Documentation Generation
    
    Generates comprehensive API specification documentation for the HP LMS BE system
    including all REST endpoints, request/response formats, authentication, and API usage examples.
    """
    
    def __init__(self):
        super().__init__(
            step_name="API Specification Documentation Generation",
            step_number=3
        )
    
    def get_model(self) -> str:
        """Use Gemini Flash for API documentation generation."""
        return "openai/local-gemini-2.5-pro"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert API documentation writer specializing in REST API documentation for NestJS/TypeScript systems.

Your task is to generate comprehensive API specification documentation for the HP LMS BE system.

IMPORTANT GUIDELINES:
- DO NOT scan files listed in .gitignore to avoid wasting tokens
- Focus on controllers, DTOs, and API endpoints
- Use Mermaid diagrams for API flow visualization
- Create documentation suitable for Quarto processing
- Follow OpenAPI/Swagger documentation standards
- Include practical examples and use cases

{self.project_config.get_logging_rules()}

Focus on:
1. Complete REST API endpoint documentation
2. Request/response schemas and validation rules
3. Authentication and authorization requirements
4. Error handling and status codes
5. API usage examples and best practices
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Generate comprehensive API specification documentation for the HP LMS BE system located at: /home/dd/work/codes/HP/hp-lms-be

Use the analysis from Step 01 and build upon the architecture documentation from Step 02.

Your tasks:
1. **API Overview**:
   - Document the API architecture and design principles
   - Explain base URL, versioning strategy, and general conventions
   - Create API flow diagrams using Mermaid

2. **Authentication & Authorization**:
   - Document authentication mechanisms (JWT, etc.)
   - Explain authorization levels and permissions
   - Show authentication flow using Mermaid sequence diagrams
   - Document token management and refresh processes

3. **Endpoint Documentation**:
   For each controller/module, document:
   - All available endpoints (GET, POST, PUT, DELETE, etc.)
   - Request parameters (path, query, body)
   - Request/response schemas with examples
   - Required headers and authentication
   - Possible error responses and status codes

4. **Data Transfer Objects (DTOs)**:
   - Document all request/response DTOs
   - Show validation rules and constraints
   - Provide example payloads
   - Explain data transformation patterns

5. **Error Handling**:
   - Document standard error response format
   - List all possible error codes and meanings
   - Provide error handling examples
   - Explain validation error responses

6. **API Usage Examples**:
   - Provide practical usage scenarios
   - Show complete request/response examples
   - Include cURL commands and code snippets
   - Document common workflows and use cases

7. **Rate Limiting & Security**:
   - Document any rate limiting policies
   - Explain security headers and CORS settings
   - Document input validation and sanitization

**Output Requirements**:
- Create a single comprehensive Markdown file: `api-specification.md`
- Use proper Markdown structure with clear headings
- Embed Mermaid diagrams for API flows and authentication
- Include JSON examples in code blocks
- Structure suitable for Quarto processing
- Save to the workspace directory

**Mermaid Diagram Types to Use**:
- API flow: `sequenceDiagram`
- Authentication flow: `sequenceDiagram`
- API architecture: `graph TD`
- Request/response flow: `flowchart LR`

Log your actions to: {self.project_config.log_full_path}
"""


def main():
    """Run the API Specification Documentation step."""
    step = ApiSpecificationStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()