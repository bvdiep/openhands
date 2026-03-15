"""
Example: Step with Custom Model
Demonstrates how to use a specific model for a step by overriding get_model()
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class ExampleStepWithGPT4(BaseStep):
    """
    Example Step: Using GPT-4 for this specific step.
    
    This demonstrates how to override get_model() to use a different model
    than the default one specified in LLM_CONFIG.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Example Step with GPT-4",
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
You are an expert AI assistant using GPT-4.

Your task is to demonstrate the per-step model configuration feature.

{self.project_config.get_logging_rules()}

Focus on:
1. Understanding the task requirements
2. Providing high-quality responses
3. Logging your actions properly
"""
    
    def get_user_prompt(self) -> str:
        return f"""
This is an example step demonstrating per-step model configuration.

Project: {self.project_config.project_name}
Workspace: {self.project_config.workspace_path}
Model being used: {self.get_model()}

Please create a simple test file to demonstrate that this step is working correctly.
Create a file named "test_model_config.txt" in the workspace with the following content:
- Step name: {self.step_name}
- Model used: {self.get_model()}
- Timestamp: [current timestamp]

Log your actions to: {self.project_config.log_full_path}
"""


class ExampleStepWithDefaultModel(BaseStep):
    """
    Example Step: Using default model from LLM_CONFIG.
    
    This demonstrates a step that doesn't override get_model(),
    so it will use the default model from LLM_CONFIG.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Example Step with Default Model",
            step_number=2
        )
    
    # No get_model() override - will use LLM_CONFIG["model"]
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert AI assistant using the default model.

Your task is to demonstrate the default model behavior.

{self.project_config.get_logging_rules()}
"""
    
    def get_user_prompt(self) -> str:
        model_name = self.get_model() or "Default from LLM_CONFIG"
        return f"""
This is an example step using the default model configuration.

Project: {self.project_config.project_name}
Workspace: {self.project_config.workspace_path}
Model being used: {model_name}

Please append to the test file "test_model_config.txt" with:
- Step name: {self.step_name}
- Model used: {model_name}
- Timestamp: [current timestamp]

Log your actions to: {self.project_config.log_full_path}
"""


class ExampleStepWithConstructorOverride(BaseStep):
    """
    Example Step: Using constructor parameter to override model.
    
    This demonstrates how to pass a model parameter to the constructor
    to dynamically select the model at runtime.
    """
    
    def __init__(self, model: str = None):
        super().__init__(
            step_name="Example Step with Constructor Override",
            step_number=3,
            model=model  # Pass model to parent constructor
        )
    
    def get_model(self) -> str:
        """
        If constructor override exists, use it.
        Otherwise, use Sonnet-4 as default for this step.
        """
        # Constructor override takes priority (handled by BaseStep)
        if self._model_override:
            return self._model_override
        
        # Otherwise, use step-specific default
        return "openai/sonnet-4"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert AI assistant with flexible model configuration.

Your task is to demonstrate dynamic model selection.

{self.project_config.get_logging_rules()}
"""
    
    def get_user_prompt(self) -> str:
        return f"""
This is an example step with flexible model configuration.

Project: {self.project_config.project_name}
Workspace: {self.project_config.workspace_path}
Model being used: {self.get_model()}

Please append to the test file "test_model_config.txt" with:
- Step name: {self.step_name}
- Model used: {self.get_model()}
- Timestamp: [current timestamp]

Log your actions to: {self.project_config.log_full_path}
"""


def main():
    """
    Demonstrate different ways to configure models for steps.
    """
    print("\n" + "=" * 60)
    print("Per-Step Model Configuration Examples")
    print("=" * 60)
    
    # Example 1: Step with custom model (GPT-4)
    print("\n1. Step with custom model (GPT-4):")
    step1 = ExampleStepWithGPT4()
    print(f"   Model: {step1.get_model()}")
    
    # Example 2: Step with default model
    print("\n2. Step with default model:")
    step2 = ExampleStepWithDefaultModel()
    print(f"   Model: {step2.get_model() or 'Default from LLM_CONFIG'}")
    
    # Example 3: Step with constructor override (Sonnet-4)
    print("\n3. Step with constructor override (default Sonnet-4):")
    step3a = ExampleStepWithConstructorOverride()
    print(f"   Model: {step3a.get_model()}")
    
    # Example 4: Step with constructor override (GPT-3.5)
    print("\n4. Step with constructor override (GPT-3.5):")
    step3b = ExampleStepWithConstructorOverride(model="openai/gpt-3.5-turbo")
    print(f"   Model: {step3b.get_model()}")
    
    print("\n" + "=" * 60)
    print("\nTo run a specific example, uncomment one of the following:")
    print("  # success = step1.run()  # Run with GPT-4")
    print("  # success = step2.run()  # Run with default model")
    print("  # success = step3a.run() # Run with Sonnet-4")
    print("  # success = step3b.run() # Run with GPT-3.5")
    print("=" * 60)
    
    # Uncomment to actually run one of the examples:
    # success = step1.run()
    # return success


if __name__ == "__main__":
    main()
