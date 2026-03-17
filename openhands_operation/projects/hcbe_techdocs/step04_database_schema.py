"""
Step 04: Database Schema Documentation for Healthcare BE
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class DatabaseSchemaStep(BaseStep):
    """
    Step 04: Database Schema Documentation
    
    Generates comprehensive database schema documentation for the Healthcare BE system
    including entity relationships, constraints, indexes, and database design patterns.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Database Schema Documentation for Healthcare BE",
            step_number=4
        )
    
    def get_model(self) -> str:
        """Use Gemini Flash for database schema documentation tasks."""
        return "gemini/gemini-3-flash-preview"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert database architect and technical writer specializing in database documentation.

Your task is to create comprehensive database schema documentation for the Healthcare BE system based on the analysis from previous steps.

IMPORTANT GUIDELINES:
- DO NOT scan files listed in .gitignore to avoid wasting tokens
- Use the analysis and previous documentation as your foundation
- Focus on database entities, relationships, constraints, and design patterns
- Create clear documentation suitable for developers and database administrators

{self.project_config.get_logging_rules()}

Focus on:
1. Database schema overview and design principles
2. Entity definitions and relationships
3. Constraints, indexes, and performance considerations
4. Migration strategies and versioning
5. Creating clear ER diagrams using Mermaid
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Based on the analysis from previous steps, create comprehensive database schema documentation for the Healthcare BE system located at: /home/dd/work/codes/HEALTHCARE/healthcare-api

Your tasks:
1. **Database Overview**:
   - Document the database architecture and design approach
   - Explain database technology stack (PostgreSQL, MySQL, etc.)
   - Document naming conventions and design principles
   - Include database configuration and connection details

2. **Entity Documentation**:
   For each database entity/table, document:
   - Table name and purpose
   - Column definitions with data types
   - Primary keys and foreign keys
   - Constraints and validation rules
   - Indexes and performance optimizations
   - Relationships with other entities

3. **Entity Relationships**:
   - Document all relationships between entities
   - Explain relationship types (one-to-one, one-to-many, many-to-many)
   - Document foreign key constraints
   - Explain cascading rules and referential integrity

4. **Database Design Patterns**:
   - Document design patterns used (normalization, denormalization)
   - Explain data modeling decisions and rationale
   - Document any special patterns (soft deletes, audit trails, etc.)
   - Include performance optimization strategies

5. **Migrations and Versioning**:
   - Document migration strategy and tools used
   - Explain database versioning approach
   - Document migration best practices
   - Include rollback strategies

6. **Mermaid Diagrams**:
   Create embedded Mermaid diagrams for:
   - Entity Relationship Diagram (ERD)
   - Database schema overview
   - Key relationships and dependencies
   - Migration flow diagram

7. **Output Requirements**:
   - Create a comprehensive Markdown document named "03_Database_Schema.md"
   - Use proper Markdown formatting with clear headings
   - Embed Mermaid diagrams directly in the Markdown
   - Include SQL examples where appropriate
   - Structure suitable for Quarto processing

8. **Documentation Structure**:
   ```
   # Healthcare BE - Database Schema
   
   ## Table of Contents
   ## 1. Database Overview
   ## 2. Design Principles
   ## 3. Entity Definitions
   ### 3.1 User Management
   ### 3.2 Healthcare Records
   ### 3.3 [Other entity groups based on analysis]
   ## 4. Entity Relationships
   ## 5. Constraints and Indexes
   ## 6. Migration Strategy
   ## 7. Performance Considerations
   ## 8. Best Practices
   ```

9. **Entity Documentation Format**:
   For each entity, use this format:
   ```markdown
   ### Users Table
   
   **Purpose**: Store user account information
   
   **Columns**:
   | Column | Type | Constraints | Description |
   |--------|------|-------------|-------------|
   | id | UUID | PRIMARY KEY | Unique user identifier |
   | email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
   | created_at | TIMESTAMP | NOT NULL | Record creation time |
   
   **Relationships**:
   - One-to-many with UserProfiles
   - Many-to-many with Roles through UserRoles
   
   **Indexes**:
   - PRIMARY KEY on id
   - UNIQUE INDEX on email
   - INDEX on created_at for sorting
   ```

10. **Mermaid ERD Example**:
    Use Mermaid erDiagram syntax for entity relationships:
    - Users ||--o{{ UserProfiles : has
    - Users }}o--o{{ Roles : assigned
    - Include entity attributes with types and constraints

Save the database schema documentation to the workspace as "03_Database_Schema.md".

Log your actions to: {self.project_config.log_full_path}
"""


def main():
    """Run the Database Schema Documentation step."""
    step = DatabaseSchemaStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()