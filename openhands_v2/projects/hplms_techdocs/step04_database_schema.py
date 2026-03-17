"""
Step 04: Database Schema Documentation Generation for HP LMS BE
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class DatabaseSchemaStep(BaseStep):
    """
    Step 04: Database Schema Documentation Generation
    
    Generates comprehensive database schema documentation for the HP LMS BE system
    including entity relationships, constraints, migrations, and database design patterns.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Database Schema Documentation Generation",
            step_number=4
        )
    
    def get_model(self) -> str:
        """Use Gemini Flash for database documentation generation."""
        return "openai/local-gemini-2.5-pro"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert database documentation writer specializing in TypeORM and relational database systems.

Your task is to generate comprehensive database schema documentation for the HP LMS BE system.

IMPORTANT GUIDELINES:
- DO NOT scan files listed in .gitignore to avoid wasting tokens
- Focus on TypeORM entities, migrations, and database configuration
- Use Mermaid ER diagrams for database visualization
- Create documentation suitable for Quarto processing
- Include database design principles and best practices
- Document relationships, constraints, and indexes

{self.project_config.get_logging_rules()}

Focus on:
1. Complete database schema with entity relationships
2. Table structures, columns, and data types
3. Constraints, indexes, and foreign keys
4. Migration history and database evolution
5. Database design patterns and optimization strategies
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Generate comprehensive database schema documentation for the HP LMS BE system located at: /home/dd/work/codes/HP/hp-lms-be

Use the analysis from Step 01 and build upon previous documentation steps.

Your tasks:
1. **Database Overview**:
   - Document database technology stack (PostgreSQL, MySQL, etc.)
   - Explain database configuration and connection settings
   - Show overall database architecture using Mermaid diagrams

2. **Entity Documentation**:
   For each TypeORM entity, document:
   - Table name and purpose
   - All columns with data types, constraints, and descriptions
   - Primary keys, foreign keys, and indexes
   - Entity relationships and associations
   - Validation rules and decorators

3. **Entity Relationships**:
   - Create comprehensive ER diagrams using Mermaid
   - Document all relationships (one-to-one, one-to-many, many-to-many)
   - Explain relationship constraints and cascade behaviors
   - Show junction tables for many-to-many relationships

4. **Database Schema Structure**:
   - Group entities by functional domains
   - Show schema organization and naming conventions
   - Document table prefixes and naming patterns
   - Explain database normalization level

5. **Migrations Documentation**:
   - Document migration history and evolution
   - Explain migration patterns and best practices
   - Show database versioning strategy
   - Document rollback procedures

6. **Indexes and Performance**:
   - Document all database indexes
   - Explain indexing strategy and performance considerations
   - Show query optimization patterns
   - Document database performance best practices

7. **Data Integrity and Constraints**:
   - Document all constraints (unique, check, foreign key)
   - Explain data validation at database level
   - Show referential integrity rules
   - Document cascade behaviors

8. **Database Design Patterns**:
   - Identify and document design patterns used
   - Explain architectural decisions
   - Document data modeling best practices
   - Show optimization strategies

**Output Requirements**:
- Create a single comprehensive Markdown file: `database-schema.md`
- Use proper Markdown structure with clear headings
- Embed Mermaid ER diagrams directly in the Markdown
- Include SQL examples where relevant
- Structure suitable for Quarto processing
- Save to the workspace directory

**Mermaid Diagram Types to Use**:
- Entity Relationship: `erDiagram`
- Database architecture: `graph TD`
- Schema organization: `flowchart LR`
- Migration flow: `sequenceDiagram`

Log your actions to: {self.project_config.log_full_path}
"""


def main():
    """Run the Database Schema Documentation step."""
    step = DatabaseSchemaStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()