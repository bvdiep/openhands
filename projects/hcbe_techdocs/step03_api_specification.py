"""
Step 03: API Specification Documentation for Healthcare BE
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class ApiSpecificationStep(BaseStep):
    """
    Step 03: API Specification Documentation
    
    Generates comprehensive API specification documentation for the Healthcare BE system
    including all endpoints, request/response formats, authentication, and API usage examples.
    """
    
    def __init__(self):
        super().__init__(
            step_name="API Specification Documentation for Healthcare BE",
            step_number=3
        )
    
    def get_model(self) -> str:
        """Use Gemini Flash for API specification documentation tasks."""
        return "gemini/gemini-3-flash-preview"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert API documentation specialist and technical writer.

Your task is to create comprehensive API specification documentation for the Healthcare BE system based on the analysis from Step 01 and architecture from Step 02.

IMPORTANT GUIDELINES:
- DO NOT scan files listed in .gitignore to avoid wasting tokens
- Use the analysis and architecture documentation as your foundation
- Focus on REST endpoints, request/response formats, and API usage
- Create clear, developer-friendly documentation with examples

{self.project_config.get_logging_rules()}

Focus on:
1. Complete API endpoint documentation
2. Request and response format specifications
3. Authentication and authorization mechanisms
4. Error handling and status codes
5. API usage examples and best practices
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Based on the analysis from Step 01 and architecture from Step 02, create comprehensive API specification documentation for the Healthcare BE system located at: /home/dd/work/codes/HEALTHCARE/healthcare-api

Your tasks:
1. **API Overview**:
   - Document the API architecture and design approach
   - Explain base URL, versioning strategy, and general conventions
   - Document common headers, parameters, and response formats
   - Include API rate limiting and usage guidelines

2. **Authentication & Authorization**:
   - Document authentication mechanisms (JWT, OAuth, etc.)
   - Explain authorization levels and permissions
   - Provide authentication flow examples
   - Document security best practices

3. **Endpoint Documentation**:
   For each API endpoint, document:
   - HTTP method and URL path
   - Request parameters (path, query, body)
   - Request body schema and examples
   - Response format and examples
   - Possible error responses and status codes
   - Required permissions/roles

4. **Data Models**:
   - Document all DTOs and data transfer objects
   - Explain data validation rules and constraints
   - Provide schema definitions and examples
   - Document relationships between models

5. **Error Handling**:
   - Document standard error response format
   - List all possible error codes and meanings
   - Provide error handling examples
   - Explain error recovery strategies

6. **Mermaid Diagrams**:
   Create embedded Mermaid diagrams for:
   - API authentication flow
   - Request/response flow diagram
   - API endpoint hierarchy
   - Data model relationships

7. **Output Requirements**:
   - Create a comprehensive Markdown document named "02_API_Specification.md"
   - Use proper Markdown formatting with clear headings
   - Embed Mermaid diagrams directly in the Markdown
   - Include code examples in appropriate language blocks
   - Structure suitable for Quarto processing

8. **Documentation Structure**:
   ```
   # Healthcare BE - API Specification
   
   ## Table of Contents
   ## 1. API Overview
   ## 2. Authentication & Authorization
   ## 3. Common Patterns
   ## 4. Endpoints
   ### 4.1 User Management
   ### 4.2 Healthcare Records
   ### 4.3 [Other modules based on analysis]
   ## 5. Data Models
   ## 6. Error Handling
   ## 7. Examples & Best Practices
   ```

9. **API Documentation Format**:
   For each endpoint, use this format:
   ```markdown
   ### POST /api/v1/users
   
   **Description**: Create a new user
   
   **Authentication**: Required (Bearer token)
   
   **Request Body**:
   ```json
   {{
     "name": "string",
     "email": "string"
   }}
   ```
   
   **Response (201)**:
   ```json
   {{
     "id": "string",
     "name": "string",
     "email": "string"
   }}
   ```
   
   **Errors**:
   - 400: Invalid request data
   - 401: Unauthorized
   - 409: Email already exists
   ```

Save the API specification documentation to the workspace as "02_API_Specification.md".

Log your actions to: {self.project_config.log_full_path}
"""


def main():
    """Run the API Specification Documentation step."""
    step = ApiSpecificationStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()