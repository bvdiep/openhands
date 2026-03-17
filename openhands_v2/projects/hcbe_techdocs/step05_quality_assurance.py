"""
Step 05: Quality Assurance for Healthcare BE Technical Documentation
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class QualityAssuranceStep(BaseStep):
    """
    Step 05: Quality Assurance
    
    Reviews and validates all generated technical documentation for the Healthcare BE system
    to ensure completeness, accuracy, consistency, and adherence to documentation standards.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Quality Assurance for Healthcare BE Documentation",
            step_number=5
        )
    
    def get_model(self) -> str:
        """Use Gemini Flash for quality assurance tasks."""
        return "gemini/gemini-3-flash-preview"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert technical documentation reviewer and quality assurance specialist.

Your task is to review and validate all generated technical documentation for the Healthcare BE system to ensure high quality, completeness, and consistency.

IMPORTANT GUIDELINES:
- Review all documentation files generated in previous steps
- Check for completeness, accuracy, and consistency
- Validate Markdown formatting and Mermaid diagrams
- Ensure documentation meets professional standards
- Provide actionable feedback and corrections

{self.project_config.get_logging_rules()}

Focus on:
1. Content completeness and accuracy
2. Documentation structure and organization
3. Markdown formatting and syntax validation
4. Mermaid diagram correctness and clarity
5. Cross-references and consistency between documents
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Review and validate all technical documentation generated for the Healthcare BE system. The documentation should include:

1. **01_Architecture.md** - System architecture documentation
2. **02_API_Specification.md** - API specification documentation  
3. **03_Database_Schema.md** - Database schema documentation

Your quality assurance tasks:

1. **Content Review**:
   - Verify completeness of each documentation section
   - Check accuracy of technical information
   - Ensure all required topics are covered
   - Validate that content matches the Healthcare BE codebase

2. **Structure and Organization**:
   - Review document structure and hierarchy
   - Check table of contents accuracy
   - Verify proper heading levels and organization
   - Ensure logical flow and readability

3. **Markdown Formatting**:
   - Validate Markdown syntax correctness
   - Check code block formatting and language tags
   - Verify table formatting and alignment
   - Ensure proper link formatting and references

4. **Mermaid Diagrams**:
   - Validate Mermaid diagram syntax
   - Check diagram clarity and accuracy
   - Ensure diagrams match documented content
   - Verify diagrams are properly embedded

5. **Consistency Check**:
   - Ensure consistent terminology across documents
   - Check cross-references between documents
   - Verify naming conventions are followed
   - Ensure consistent formatting style

6. **Completeness Validation**:
   - Architecture document covers all major components
   - API specification includes all endpoints
   - Database schema covers all entities and relationships
   - All sections have appropriate level of detail

7. **Quality Improvements**:
   - Identify areas for improvement
   - Suggest additional content if needed
   - Recommend formatting enhancements
   - Propose better organization if applicable

8. **Output Requirements**:
   Create a comprehensive quality assurance report named "QA_Report.md" that includes:
   - Overall assessment of documentation quality
   - Detailed review of each document
   - List of issues found and their severity
   - Recommendations for improvements
   - Validation checklist with pass/fail status

9. **QA Report Structure**:
   ```
   # Healthcare BE Documentation - Quality Assurance Report
   
   ## Executive Summary
   ## Overall Assessment
   ## Document Reviews
   ### Architecture Documentation Review
   ### API Specification Review  
   ### Database Schema Review
   ## Issues and Recommendations
   ### Critical Issues
   ### Minor Issues
   ### Improvement Suggestions
   ## Validation Checklist
   ## Conclusion and Next Steps
   ```

10. **Issue Classification**:
    - **Critical**: Missing essential content, broken formatting, incorrect information
    - **Major**: Incomplete sections, inconsistent terminology, unclear explanations
    - **Minor**: Formatting improvements, additional examples, style enhancements

After completing the review, if any critical or major issues are found, provide specific corrections and improvements for each document.

Save the quality assurance report to the workspace as "QA_Report.md".

Log your actions to: {self.project_config.log_full_path}
"""


def main():
    """Run the Quality Assurance step."""
    step = QualityAssuranceStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()