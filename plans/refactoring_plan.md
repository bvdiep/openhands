# Refactoring Plan: Unified Task Runner

This plan outlines the design and implementation of a reusable runner in `openhands_v2/runner.py` to eliminate boilerplate code in `run_*.py` scripts.

## 1. Problem Statement
Existing `run_*.py` files contain significant boilerplate code (approx. 50-60 lines each) for:
- LLM initialization (hardcoded or semi-dynamic).
- Agent and Conversation setup.
- Manual workspace directory management.
- Repeated error handling (`try-except` blocks).
- Manual logging/printing of status.

## 2. Proposed Solution
Create a centralized `TaskRunner` class and a `run_task` convenience function in `openhands_v2/runner.py`.

### 2.1 Core Components
- **`TaskRunner` Class**: Encapsulates the configuration and execution logic.
- **`run_task` Function**: A simplified entry point for functional-style usage.
- **Default Integration**: Automatically uses settings from `openhands_v2/config.py`.

### 2.2 The 5-Step Execution Flow
The runner will automate the following flow:
1. **Start**: Log the initiation, workspace, and model being used.
2. **Setup**: Initialize LLM, Agent, and Conversation with proper defaults or overrides.
3. **Dispatch**: Send the task prompt to the agent.
4. **Execution**: Execute the agent's action loop until completion.
5. **Reporting**: Provide clear success/failure feedback and clean up resources (close conversation).

## 3. Proposed API Design (`openhands_v2/runner.py`)

```python
from typing import List, Optional, Dict, Any
import os
import traceback
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.terminal import TerminalTool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.browser_use import BrowserToolSet

# Integration with existing config
from .config import LLM_CONFIG

class TaskRunner:
    def __init__(
        self,
        workspace: str,
        model: Optional[str] = None,
        tools: Optional[List[Tool]] = None,
        agent_name: str = "OpenHands-Agent",
        mcp_config: Optional[Dict[str, Any]] = None
    ):
        self.workspace = os.path.abspath(workspace)
        self.model = model or LLM_CONFIG.get("model")
        
        # Default tools if none provided
        self.tools = tools if tools is not None else [
            Tool(name=TerminalTool.name),
            Tool(name=FileEditorTool.name),
            Tool(name=BrowserToolSet.name)
        ]
        
        # Initialize LLM using shared config
        self.llm = LLM(
            model=self.model,
            base_url=LLM_CONFIG.get("base_url"),
            api_key=LLM_CONFIG.get("api_key"),
            temperature=LLM_CONFIG.get("temperature", 0.0),
        )
        
        # Setup Agent
        self.agent = Agent(
            llm=self.llm,
            tools=self.tools,
            name=agent_name,
            mcp_config=mcp_config
        )
        
        # Ensure workspace exists
        os.makedirs(self.workspace, exist_ok=True)
            
    def run(self, task_prompt: str, success_message: str = "Nhiệm vụ hoàn tất!"):
        print(f"🚀 OpenHands Runner starting at: {self.workspace}")
        print(f"🤖 Model: {self.model}")
        
        conversation = None
        try:
            conversation = Conversation(agent=self.agent, workspace=self.workspace)
            conversation.send_message(task_prompt)
            
            print("--- Đang thực thi ---")
            conversation.run()
            
            print(f"\n✅ {success_message}")
            return True
            
        except Exception as e:
            print(f"\n❌ Lỗi thực thi: {e}")
            traceback.print_exc()
            return False
            
        finally:
            if conversation:
                conversation.close()

def run_task(task_prompt: str, **kwargs):
    """
    Convenience function for quick task execution.
    Usage:
        run_task(task_prompt="...", workspace="./path", model="...")
    """
    success_msg = kwargs.pop('success_message', "Nhiệm vụ hoàn tất!")
    runner = TaskRunner(**kwargs)
    return runner.run(task_prompt, success_message=success_msg)
```

## 4. Refactoring Example

### Before (`run_mcp_internet.py` - 61 lines)
```python
import os
from openhands.sdk import LLM, Agent, Conversation, Tool
# ... multiple imports ...

llm = LLM(model="openai/sonnet-4", ...)
agent = Agent(llm=llm, tools=[...])
cwd = os.path.join(os.getcwd(), "mcp_internet")
# ... manual dir creation ...
conversation = Conversation(agent=agent, workspace=cwd)

task_prompt = "..."

try:
    conversation.send_message(task_prompt)
    conversation.run() 
    print("\n✅ Nhiệm vụ hoàn tất!")
except Exception as e:
    print(f"❌ Lỗi: {e}")
```

### After (Estimated 10-15 lines)
```python
from openhands_v2.runner import run_task

run_task(
    workspace="./mcp_internet",
    model="openai/sonnet-4", # Optional override
    task_prompt="""
    Hãy xây dựng một MCP Server bằng Python...
    """,
    success_message="Kiểm tra thư mục mcp_internet."
)
```

## 5. Benefits
1. **DRY (Don't Repeat Yourself)**: Logic for initialization and error handling is defined once.
2. **Consistency**: All standalone scripts will behave and report status in the same way.
3. **Maintainability**: Changing the default model or adding a global tool requires editing only one file (`config.py` or `runner.py`).
4. **Readability**: Focus on the *task* (prompt and workspace) rather than the plumbing.

## 6. Implementation Steps
1. Create `openhands_v2/runner.py`.
2. Update `openhands_v2/config.py` to ensure all necessary defaults are exposed.
3. Refactor one `run_*.py` file as a pilot.
4. Batch refactor remaining `run_*.py` files.
