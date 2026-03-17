"""
Step 05: Quality Assurance and Documentation Review for HP LMS BE
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class QualityAssuranceStep(BaseStep):
    """
    Step 05: Quality Assurance and Documentation Review
    
    Reviews and validates all generated documentation for completeness, accuracy,
    and consistency. Ensures proper formatting, cross-references, and Quarto compatibility.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Quality Assurance and Documentation Review",
            step_number=5
        )
    
    def get_model(self) -> str:
        """Use Gemini Flash for quality assurance and review."""
        return "openai/local-gemini-2.5-pro"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert technical documentation reviewer and quality assurance specialist.

Your task is to review and validate all generated documentation for the HP LMS BE system.

IMPORTANT GUIDELINES:
- Review all generated documentation files for completeness and accuracy
- Ensure proper Markdown formatting and Quarto compatibility
- Validate Mermaid diagrams syntax and rendering
- Check cross-references and internal links
- Ensure consistency across all documentation sections
- Verify that documentation matches the actual codebase

{self.project_config.get_logging_rules()}

Focus on:
1. Documentation completeness and coverage
2. Technical accuracy and consistency
3. Formatting and structure validation
4. Mermaid diagram syntax and rendering
5. Cross-references and navigation
6. Quarto compatibility and processing
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Review and validate all generated documentation for the HP LMS BE system.

Your tasks:
1. **Documentation Review**:
   - Review all generated Markdown files in the workspace
   - Check architecture-documentation.md for completeness
   - Validate api-specification.md for accuracy
   - Review database-schema.md for technical correctness

2. **Content Validation**:
   - Verify that documentation matches the actual codebase at /home/dd/work/codes/HP/hp-lms-be
   - Check for missing components, endpoints, or entities
   - Validate technical details and implementation specifics
   - Ensure all major system components are documented

3. **Format and Structure Review**:
   - Validate Markdown syntax and formatting
   - Check heading hierarchy and structure
   - Ensure proper code block formatting
   - Validate table structures and lists

4. **Mermaid Diagram Validation**:
   - Check all Mermaid diagram syntax
   - Ensure diagrams render correctly
   - Validate diagram types and structures
   - Check for proper diagram labeling and clarity

5. **Cross-Reference Validation**:
   - Check internal links and references
   - Ensure consistent terminology across documents
   - Validate section references and navigation
   - Check for broken or missing links

6. **Quarto Compatibility**:
   - Ensure all files are compatible with Quarto processing
   - Check for proper YAML frontmatter if needed
   - Validate code block languages and syntax highlighting
   - Ensure proper figure and table referencing

7. **Quality Improvements**:
   - Identify gaps or missing information
   - Suggest improvements for clarity and completeness
   - Fix any formatting or syntax issues
   - Enhance documentation structure if needed

8. **Final Documentation Package**:
   - Create a comprehensive index or table of contents
   - Generate a README.md for the documentation package
   - Ensure all files are properly organized
   - Create a final quality assurance report

**Output Requirements**:
- Review and fix all existing documentation files
- Create a comprehensive `README.md` for the documentation package
- Generate a `quality-assurance-report.md` with findings and improvements
- Ensure all files are Quarto-ready and properly formatted
- Save all files to the workspace directory

**Quality Checklist**:
- [ ] All major system components documented
- [ ] API endpoints complete and accurate
- [ ] Database schema matches entities
- [ ] Mermaid diagrams render correctly
- [ ] Markdown formatting is consistent
- [ ] Cross-references work properly
- [ ] Documentation is Quarto-compatible
- [ ] Technical accuracy verified

Log your actions to: {self.project_config.log_full_path}
"""


def main():
    """Run the Quality Assurance and Documentation Review step."""
    step = QualityAssuranceStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()