"""
Base class for all pipeline steps.
Provides common functionality and enforces consistent structure.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from openhands.sdk import LLM, Conversation, Agent, Tool
from openhands.tools.browser_use import BrowserToolSet
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.terminal import TerminalTool

from .config import LLM_CONFIG, get_project_config


class BaseStep(ABC):
    """
    Base class for all pipeline steps.
    Each step should inherit from this and implement required methods.
    
    MCP Support:
        Override get_mcp_config() to enable MCP servers for this step.
        Example:
            def get_mcp_config(self) -> Dict[str, Any]:
                return {
                    "servers": {
                        "internet-search": {
                            "type": "stdio",
                            "command": "/path/to/python",
                            "args": ["/path/to/server.py"],
                            "env": {
                                "API_KEY": "value"
                            }
                        }
                    }
                }
    """
    
    def __init__(self, step_name: str, step_number: int, model: Optional[str] = None):
        """
        Initialize a step.
        
        Args:
            step_name: Human-readable name of the step
            step_number: Sequential number of the step (01, 02, 03, etc.)
            model: Optional model name to override get_model() (e.g., "openai/gpt-4")
        """
        self.step_name = step_name
        self.step_number = step_number
        self._model_override = model  # Store model override
        self.llm = None
        self.agent = None
        self.conversation = None
        
        # Lazy load project configuration
        self._project_config = None
    
    @property
    def project_config(self):
        """Lazy load project configuration."""
        if self._project_config is None:
            self._project_config = get_project_config()
        return self._project_config
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Return the system prompt for this step.
        Must be implemented by each step.
        """
        pass
    
    @abstractmethod
    def get_user_prompt(self) -> str:
        """
        Return the user prompt/instructions for this step.
        Must be implemented by each step.
        """
        pass
    
    def get_tools(self) -> List[Tool]:
        """
        Return the list of tools for this step.
        Can be overridden if a step needs different tools.
        """
        return [
            Tool(name=TerminalTool.name),
            Tool(name=FileEditorTool.name),
            Tool(name=BrowserToolSet.name)
        ]
    
    def get_model(self) -> Optional[str]:
        """
        Return the model name for this step.
        Override this method in subclass to use a different model.
        
        Returns:
            str: Model name (e.g., "openai/gpt-4", "openai/sonnet-4")
            None: Use default model from LLM_CONFIG
        
        Priority (handled by Python inheritance):
            1. Constructor override (_model_override) - checked in base class
            2. Subclass override - subclass method replaces this entirely
            3. None (default) - use LLM_CONFIG["model"]
        
        Examples:
            # Use GPT-4 for this step
            def get_model(self) -> str:
                return "openai/gpt-4"
            
            # Use default model (don't override)
            # def get_model(self) -> Optional[str]:
            #     return None
        """
        # If constructor override provided, use it
        if self._model_override:
            return self._model_override
        # Otherwise return None (subclasses can override entire method)
        return None  # Default: use LLM_CONFIG["model"]
    
    def setup_llm(self) -> LLM:
        """Initialize and return LLM instance."""
        # Get model from step-specific config or fallback to default
        model = self.get_model() or LLM_CONFIG["model"]
        
        self.llm = LLM(
            model=model,
            api_key=LLM_CONFIG["api_key"],
            base_url=LLM_CONFIG["base_url"],
            temperature=LLM_CONFIG["temperature"]
        )
        return self.llm
    
    def get_mcp_config(self) -> Optional[Dict[str, Any]]:
        """
        Return MCP (Model Context Protocol) configuration for this step.
        Override this method to enable MCP servers for this step.
        
        Returns:
            Dict[str, Any]: MCP configuration with servers
                Example:
                {
                    "servers": {
                        "server-name": {
                            "type": "stdio",  # or "sse", "http"
                            "command": "/path/to/python",
                            "args": ["/path/to/server.py"],
                            "env": {
                                "KEY": "value"
                            },
                            # For sse/http:
                            "url": "http://example.com/mcp",
                            "headers": {
                                "Authorization": "Bearer token"
                            }
                        }
                    }
                }
            None: No MCP servers needed (default)
        
        Examples:
            # Example 1: Internet Search MCP
            def get_mcp_config(self) -> Dict[str, Any]:
                import os
                return {
                    "servers": {
                        "internet-search": {
                            "type": "stdio",
                            "command": os.path.join(os.getcwd(), "apps", "mcp_internet", ".venv", "bin", "python"),
                            "args": [os.path.join(os.getcwd(), "apps", "mcp_internet", "server.py")],
                            "env": {
                                "SERPER_API_KEY": os.getenv("SERPER_API_KEY", ""),
                                "VOYAGE_API_KEY": os.getenv("VOYAGE_API_KEY", ""),
                                "PYTHONPATH": os.path.join(os.getcwd(), "apps", "mcp_internet")
                            }
                        }
                    }
                }
            
            # Example 2: No MCP (default)
            # Don't override this method or return None
        
        # Example 3: Multiple MCP servers
        # Add more servers to the "servers" dict
        """
        return None  # Default: no MCP servers
    
    def setup_agent(self) -> Agent:
        """Initialize and return Agent instance with MCP support."""
        if not self.llm:
            self.setup_llm()
        
        # Get MCP configuration if available
        mcp_config = self.get_mcp_config()
        
        # Build agent kwargs
        agent_kwargs = {
            "llm": self.llm,
            "tools": self.get_tools(),
            "system_prompt": self.get_system_prompt()
        }
        
        # Add MCP config if provided
        if mcp_config:
            agent_kwargs["mcp_config"] = mcp_config
        
        self.agent = Agent(**agent_kwargs)
        return self.agent
    
    def setup_conversation(self) -> Conversation:
        """Initialize and return Conversation instance."""
        if not self.agent:
            self.setup_agent()
        
        self.conversation = Conversation(
            agent=self.agent,
            workspace=self.project_config.workspace_path,
            persistence_dir=self.project_config.persistence_dir,
            conversation_id=self.project_config.conversation_id
        )
        return self.conversation
    
    def run(self) -> bool:
        """
        Execute the step.
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"PROJECT: {self.project_config.project_name}")
        print(f"STEP {self.step_number:02d}: {self.step_name}")
        print(f"{'='*60}\n")
        
        try:
            # Setup
            self.setup_conversation()
            
            # Get and send prompt
            user_prompt = self.get_user_prompt()
            print(f"--- Đang thực thi: {self.step_name} ---")
            
            self.conversation.send_message(user_prompt)
            self.conversation.run()
            
            print(f"\n[Thành công]: {self.step_name} hoàn tất.")
            print(f"--- Đã tự động lưu trạng thái vào {self.project_config.persistence_dir} ---")
            
            return True
            
        except Exception as e:
            import traceback
            print(f"[Lỗi]: {e}")
            print(f"Stack trace:\n{traceback.format_exc()}")
            return False
            
        finally:
            # Cleanup
            if self.conversation:
                self.conversation.close()
            print(f"--- Đã đóng kết nối Step {self.step_number:02d} ---\n")
    
    def __str__(self) -> str:
        return f"Step {self.step_number:02d}: {self.step_name}"
