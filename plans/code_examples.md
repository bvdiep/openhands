# Code Examples: Per-Step Model Configuration

## Example 1: Step với Custom Model (GPT-4)

```python
"""
Example: Step with Custom Model
Demonstrates how to use a specific model for a step by overriding get_model()
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(parent_dir))

from openhands_operation.base_step import BaseStep


class Step01PlanningWithGPT4(BaseStep):
    """
    Step 01: Planning & Analysis using GPT-4
    
    This step uses GPT-4 for better reasoning and planning capabilities.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Planning & Analysis (GPT-4)",
            step_number=1
        )
    
    def get_model(self) -> str:
        """
        Override to use GPT-4 for this step.
        GPT-4 is better for complex reasoning and planning tasks.
        """
        return "openai/gpt-4"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert software architect and planner.

Your task is to analyze requirements and create a detailed implementation plan.

{self.project_config.get_logging_rules()}

Focus on:
1. Understanding the requirements thoroughly
2. Breaking down the work into clear, actionable steps
3. Identifying potential challenges and solutions
4. Creating a realistic timeline
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Please analyze the following project and create a detailed implementation plan:

Project: {self.project_config.project_name}
Target: {self.project_config.target_url}
Workspace: {self.project_config.workspace_path}

Tech Stack:
{self._format_tech_stack()}

Create a comprehensive plan that includes:
1. Project overview and goals
2. Technical architecture
3. Implementation phases
4. Key features and components
5. Potential challenges and mitigation strategies

Save the plan to: {self.project_config.plan_full_path}
"""
    
    def _format_tech_stack(self) -> str:
        """Format tech stack for display."""
        return "\n".join([
            f"- {key}: {value}"
            for key, value in self.project_config.tech_stack.items()
        ])


def main():
    """Run Step 01 with GPT-4."""
    step = Step01PlanningWithGPT4()
    
    print(f"Model being used: {step.get_model()}")
    print(f"This step will use GPT-4 instead of the default model from LLM_CONFIG")
    
    success = step.run()
    
    if success:
        print("\n✓ Step 01 completed successfully with GPT-4.")
    else:
        print("\n✗ Step 01 failed.")
    
    return success


if __name__ == "__main__":
    main()
```

## Example 2: Step với Default Model

```python
"""
Example: Step with Default Model
Demonstrates a step that uses the default model from LLM_CONFIG
"""
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(parent_dir))

from openhands_operation.base_step import BaseStep


class Step02ImplementationDefault(BaseStep):
    """
    Step 02: Implementation using default model
    
    This step doesn't override get_model(), so it will use
    the default model from LLM_CONFIG.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Implementation (Default Model)",
            step_number=2
        )
    
    # No get_model() override - will use LLM_CONFIG["model"]
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert software developer.

Your task is to implement the features according to the plan.

{self.project_config.get_logging_rules()}

Focus on:
1. Writing clean, maintainable code
2. Following best practices
3. Implementing all required features
4. Testing as you go
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Please implement the features for this project:

Project: {self.project_config.project_name}
Workspace: {self.project_config.workspace_path}
Plan: {self.project_config.plan_full_path}

Read the plan and implement all features step by step.
Log your progress to: {self.project_config.log_full_path}
"""


def main():
    """Run Step 02 with default model."""
    step = Step02ImplementationDefault()
    
    print(f"Model being used: {step.get_model() or 'Default from LLM_CONFIG'}")
    print(f"This step will use the default model from LLM_CONFIG")
    
    success = step.run()
    
    if success:
        print("\n✓ Step 02 completed successfully with default model.")
    else:
        print("\n✗ Step 02 failed.")
    
    return success


if __name__ == "__main__":
    main()
```

## Example 3: Step với Model Override qua Constructor (Optional)

```python
"""
Example: Step with Constructor Model Override
Demonstrates how to override model via constructor parameter
"""
import sys
from pathlib import Path
from typing import Optional

parent_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(parent_dir))

from openhands_operation.base_step import BaseStep


class Step03TestingFlexible(BaseStep):
    """
    Step 03: Testing with flexible model configuration
    
    This step can accept a model parameter in constructor,
    allowing dynamic model selection.
    """
    
    def __init__(self, model: Optional[str] = None):
        super().__init__(
            step_name="Testing (Flexible Model)",
            step_number=3,
            model=model  # Pass to parent if BaseStep supports it
        )
    
    def get_model(self) -> Optional[str]:
        """
        Return model if specified in constructor.
        Otherwise, use Sonnet-4 as default for this step.
        """
        # If constructor override exists, use it
        if hasattr(self, '_model_override') and self._model_override:
            return self._model_override
        
        # Otherwise, use step-specific default
        return "openai/sonnet-4"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert QA engineer.

Your task is to write comprehensive tests for the implemented features.

{self.project_config.get_logging_rules()}

Focus on:
1. Unit tests for all components
2. Integration tests for key workflows
3. Edge cases and error handling
4. Test coverage and quality
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Please write comprehensive tests for this project:

Project: {self.project_config.project_name}
Workspace: {self.project_config.workspace_path}

Write tests for all implemented features.
Ensure good test coverage and quality.
"""


def main():
    """Run Step 03 with different model configurations."""
    
    # Example 1: Use step's default model (Sonnet-4)
    print("=" * 60)
    print("Example 1: Using step's default model (Sonnet-4)")
    print("=" * 60)
    step1 = Step03TestingFlexible()
    print(f"Model: {step1.get_model()}")
    
    # Example 2: Override with GPT-4
    print("\n" + "=" * 60)
    print("Example 2: Override with GPT-4")
    print("=" * 60)
    step2 = Step03TestingFlexible(model="openai/gpt-4")
    print(f"Model: {step2.get_model()}")
    
    # Example 3: Override with GPT-3.5 (cheaper for simple tests)
    print("\n" + "=" * 60)
    print("Example 3: Override with GPT-3.5 (cheaper)")
    print("=" * 60)
    step3 = Step03TestingFlexible(model="openai/gpt-3.5-turbo")
    print(f"Model: {step3.get_model()}")
    
    # Run one of them
    success = step1.run()
    
    if success:
        print("\n✓ Step 03 completed successfully.")
    else:
        print("\n✗ Step 03 failed.")
    
    return success


if __name__ == "__main__":
    main()
```

## Example 4: Mixed Models trong Pipeline

```python
"""
Example: Pipeline with Mixed Models
Demonstrates a complete pipeline using different models for different steps
"""
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(parent_dir))

from openhands_operation.base_step import BaseStep


class Step01Planning(BaseStep):
    """Planning with GPT-4 for better reasoning."""
    
    def __init__(self):
        super().__init__(step_name="Planning", step_number=1)
    
    def get_model(self) -> str:
        return "openai/gpt-4"  # Best for planning
    
    def get_system_prompt(self) -> str:
        return "You are a planning expert..."
    
    def get_user_prompt(self) -> str:
        return "Create a detailed plan..."


class Step02Implementation(BaseStep):
    """Implementation with Sonnet-4 for better code generation."""
    
    def __init__(self):
        super().__init__(step_name="Implementation", step_number=2)
    
    def get_model(self) -> str:
        return "openai/sonnet-4"  # Best for coding
    
    def get_system_prompt(self) -> str:
        return "You are a coding expert..."
    
    def get_user_prompt(self) -> str:
        return "Implement the features..."


class Step03SimpleTask(BaseStep):
    """Simple task with GPT-3.5 to save costs."""
    
    def __init__(self):
        super().__init__(step_name="Simple Task", step_number=3)
    
    def get_model(self) -> str:
        return "openai/gpt-3.5-turbo"  # Cheaper for simple tasks
    
    def get_system_prompt(self) -> str:
        return "You are a helpful assistant..."
    
    def get_user_prompt(self) -> str:
        return "Perform simple file operations..."


class Step04Review(BaseStep):
    """Review with default model from LLM_CONFIG."""
    
    def __init__(self):
        super().__init__(step_name="Review", step_number=4)
    
    # No get_model() override - uses LLM_CONFIG
    
    def get_system_prompt(self) -> str:
        return "You are a code reviewer..."
    
    def get_user_prompt(self) -> str:
        return "Review the implementation..."


def main():
    """Run pipeline with mixed models."""
    steps = [
        Step01Planning(),
        Step02Implementation(),
        Step03SimpleTask(),
        Step04Review()
    ]
    
    print("\n" + "=" * 60)
    print("Pipeline with Mixed Models")
    print("=" * 60)
    
    for step in steps:
        model = step.get_model() or "Default (LLM_CONFIG)"
        print(f"Step {step.step_number}: {step.step_name}")
        print(f"  Model: {model}")
    
    print("\n" + "=" * 60)
    print("Running pipeline...")
    print("=" * 60)
    
    for step in steps:
        print(f"\nRunning {step.step_name}...")
        success = step.run()
        
        if not success:
            print(f"\n✗ Pipeline failed at {step.step_name}")
            return False
    
    print("\n✓ Pipeline completed successfully!")
    return True


if __name__ == "__main__":
    main()
```

## Example 5: Dynamic Model Selection

```python
"""
Example: Dynamic Model Selection
Demonstrates selecting model based on task complexity or other factors
"""
import sys
from pathlib import Path
from typing import Optional

parent_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(parent_dir))

from openhands_operation.base_step import BaseStep


class SmartStep(BaseStep):
    """
    A smart step that selects model based on task complexity.
    """
    
    def __init__(self, task_complexity: str = "medium"):
        """
        Initialize with task complexity.
        
        Args:
            task_complexity: "simple", "medium", or "complex"
        """
        super().__init__(
            step_name=f"Smart Step ({task_complexity})",
            step_number=1
        )
        self.task_complexity = task_complexity
    
    def get_model(self) -> str:
        """
        Select model based on task complexity.
        """
        model_map = {
            "simple": "openai/gpt-3.5-turbo",  # Cheap and fast
            "medium": "openai/sonnet-4",        # Balanced
            "complex": "openai/gpt-4"           # Best quality
        }
        
        return model_map.get(self.task_complexity, "openai/sonnet-4")
    
    def get_system_prompt(self) -> str:
        return f"""
You are an AI assistant handling a {self.task_complexity} task.

{self.project_config.get_logging_rules()}
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Task complexity: {self.task_complexity}
Model selected: {self.get_model()}

Please complete the task accordingly.
"""


def main():
    """Demonstrate dynamic model selection."""
    
    # Simple task - use cheap model
    simple_step = SmartStep(task_complexity="simple")
    print(f"Simple task using: {simple_step.get_model()}")
    
    # Medium task - use balanced model
    medium_step = SmartStep(task_complexity="medium")
    print(f"Medium task using: {medium_step.get_model()}")
    
    # Complex task - use best model
    complex_step = SmartStep(task_complexity="complex")
    print(f"Complex task using: {complex_step.get_model()}")
    
    # Run one of them
    success = medium_step.run()
    
    return success


if __name__ == "__main__":
    main()
```

## Summary

Các examples trên minh họa:

1. **Example 1**: Override `get_model()` để sử dụng model cụ thể (GPT-4)
2. **Example 2**: Không override, sử dụng default model từ LLM_CONFIG
3. **Example 3**: Override model qua constructor (flexible)
4. **Example 4**: Pipeline với nhiều steps sử dụng models khác nhau
5. **Example 5**: Dynamic model selection dựa trên task complexity

Tất cả các cách đều hợp lệ và có thể kết hợp tùy theo nhu cầu cụ thể của project.
