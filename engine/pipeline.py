"""
Pipeline Runner - Shared orchestrator for all projects
Manages step execution, dependencies, and provides easy CLI interface.
This is a shared module - each project should have its own pipeline.py that uses this.
"""
import sys
from typing import Dict, List, Optional, Type

from .base_step import BaseStep


class StepRegistry:
    """Registry for all available steps."""
    
    def __init__(self):
        self._steps: Dict[int, Type[BaseStep]] = {}
        self._step_names: Dict[int, str] = {}
        self._register_default_steps()
    
    def _register_default_steps(self):
        """
        Register the default steps.
        Override this method in project-specific registries.
        """
        pass
    
    def register_step(self, step_number: int, step_class: Type[BaseStep], step_name: str):
        """Register a new step."""
        self._steps[step_number] = step_class
        self._step_names[step_number] = step_name
    
    def get_step(self, step_number: int) -> Optional[BaseStep]:
        """Get a step instance by number."""
        if step_number in self._steps:
            return self._steps[step_number]()
        return None
    
    def list_steps(self) -> List[tuple]:
        """List all registered steps."""
        return [(num, name) for num, name in sorted(self._step_names.items())]
    
    def get_available_steps(self) -> List[int]:
        """Get list of available step numbers."""
        return sorted(self._steps.keys())


class PipelineRunner:
    """Main pipeline runner."""
    
    def __init__(self):
        self.registry = StepRegistry()
    
    def run_step(self, step_number: int) -> bool:
        """Run a specific step."""
        step = self.registry.get_step(step_number)
        if not step:
            print(f"❌ Step {step_number:02d} không tồn tại!")
            return False
        
        return step.run()
    
    def run_steps(self, start_step: int = 1, end_step: Optional[int] = None) -> bool:
        """Run a range of steps."""
        available_steps = self.registry.get_available_steps()
        
        if not available_steps:
            print("❌ Không có steps nào được đăng ký!")
            return False
        
        if end_step is None:
            end_step = max(available_steps)
        
        # Validate range
        if start_step not in available_steps:
            print(f"❌ Step {start_step:02d} không tồn tại!")
            return False
        
        steps_to_run = [s for s in available_steps if start_step <= s <= end_step]
        
        print(f"\n🚀 Chạy pipeline từ Step {start_step:02d} đến Step {end_step:02d}")
        print(f"Steps sẽ chạy: {steps_to_run}")
        
        for step_num in steps_to_run:
            success = self.run_step(step_num)
            if not success:
                print(f"\n❌ Pipeline dừng tại Step {step_num:02d}")
                return False
        
        print(f"\n✅ Pipeline hoàn tất thành công!")
        return True
    
    def list_available_steps(self):
        """List all available steps."""
        print("\n📋 Các Steps có sẵn:")
        print("=" * 50)
        
        steps = self.registry.list_steps()
        if not steps:
            print("  (Chưa có steps nào được đăng ký)")
        else:
            for step_num, step_name in steps:
                print(f"  Step {step_num:02d}: {step_name}")
        
        print("=" * 50)
