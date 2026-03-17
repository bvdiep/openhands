"""
Step Example: Using MCP (Model Context Protocol) in a Step

This example demonstrates how to use MCP servers in a step.
MCP allows the agent to use external tools like internet search, 
meeting minutes transcription, and more.

Usage:
    This is a template showing how to use MCP in a step.
    Copy and modify for your own steps.
"""
import os
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class MCPStepExample(BaseStep):
    """
    Example Step with MCP support.
    
    This step demonstrates how to configure and use MCP servers.
    The MCP server provides additional tools beyond the default ones.
    """
    
    def __init__(self):
        super().__init__(
            step_name="MCP Example Step",
            step_number=1
        )
    
    def get_mcp_config(self):
        """
        Configure MCP servers for this step.
        
        This example shows how to configure the internet-search MCP server.
        The MCP server provides the 'internet_search' tool.
        
        Required environment variables:
            - SERPER_API_KEY: API key for Serper search (get from https://serper.dev)
            - VOYAGE_API_KEY: API key for VoyageAI reranking (get from https://voyageai.com)
        
        Returns:
            dict: MCP configuration
        """
        return {
            "servers": {
                "internet-search": {
                    "type": "stdio",
                    "command": os.getenv(
                        "MCP_INTERNET_PYTHON",
                        "/home/dd/work/diep/openhands/mcp_internet/.venv/bin/python"
                    ),
                    "args": [
                        os.getenv(
                            "MCP_INTERNET_SERVER",
                            "/home/dd/work/diep/openhands/mcp_internet/server.py"
                        )
                    ],
                    "env": {
                        "SERPER_API_KEY": os.getenv("SERPER_API_KEY", ""),
                        "VOYAGE_API_KEY": os.getenv("VOYAGE_API_KEY", ""),
                        "PYTHONPATH": os.getenv(
                            "MCP_INTERNET_PATH",
                            "/home/dd/work/diep/openhands/mcp_internet"
                        )
                    }
                }
            }
        }
    
    def get_system_prompt(self) -> str:
        return f"""
You are an AI assistant with access to MCP tools.

Available MCP Tools:
- internet_search: Search the web and get relevant information with sources

The internet_search tool will:
1. Search using Serper API
2. Rerank results using VoyageAI
3. Crawl and extract clean content

Instructions:
- Always use the internet_search tool when you need current information
- Cite your sources when providing information
- Be thorough in your research

{self.project_config.get_logging_rules()}
"""
    
    def get_user_prompt(self) -> str:
        return """
Research the latest developments in AI agents and MCP (Model Context Protocol).

Provide a comprehensive summary including:
1. What is MCP and how does it work?
2. Latest trends in AI agent frameworks
3. How MCP is being used in production applications
4. Future outlook for MCP and AI agents

Use the internet_search tool to find current information.
"""


class NoMCPStepExample(BaseStep):
    """
    Example Step WITHOUT MCP (Default behavior)
    
    This is how you create a step without MCP.
    Simply don't override get_mcp_config() or return None.
    """
    
    def __init__(self):
        super().__init__(
            step_name="No MCP Example Step",
            step_number=2
        )
    
    # Don't override get_mcp_config() - this step won't use MCP
    
    def get_system_prompt(self) -> str:
        return f"""
You are a coding assistant.

Available Tools:
- Terminal: Run commands in the terminal
- FileEditor: Read and edit files
- Browser: Browse websites

{self.project_config.get_logging_rules()}
"""
    
    def get_user_prompt(self) -> str:
        return """
Create a simple Python script that prints "Hello, World!" to the console.

Save it as hello.py in the workspace.
"""


class MultiMCPStepExample(BaseStep):
    """
    Example Step with Multiple MCP servers
    
    This demonstrates how to configure multiple MCP servers.
    """
    
    def __init__(self):
        super().__init__(
            step_name="Multi-MCP Example Step",
            step_number=3
        )
    
    def get_mcp_config(self):
        """
        Configure multiple MCP servers.
        
        You can add as many MCP servers as needed.
        Each server will provide its own set of tools.
        """
        config = {
            "servers": {}
        }
        
        # Add internet-search MCP if environment variables are set
        if os.getenv("SERPER_API_KEY") and os.getenv("VOYAGE_API_KEY"):
            config["servers"]["internet-search"] = {
                "type": "stdio",
                "command": os.getenv(
                    "MCP_INTERNET_PYTHON",
                    "/home/dd/work/diep/openhands/mcp_internet/.venv/bin/python"
                ),
                "args": [
                    os.getenv(
                        "MCP_INTERNET_SERVER",
                        "/home/dd/work/diep/openhands/mcp_internet/server.py"
                    )
                ],
                "env": {
                    "SERPER_API_KEY": os.getenv("SERPER_API_KEY", ""),
                    "VOYAGE_API_KEY": os.getenv("VOYAGE_API_KEY", ""),
                    "PYTHONPATH": os.getenv(
                        "MCP_INTERNET_PATH",
                        "/home/dd/work/diep/openhands/mcp_internet"
                    )
                }
            }
        
        # Add meeting minutes MCP if configured
        if os.getenv("OPENAI_API_KEY"):
            config["servers"]["meeting-minutes"] = {
                "type": "stdio",
                "command": os.getenv(
                    "MCP_MEETING_PYTHON",
                    "/home/dd/work/diep/openhands/mcp_meeting_minutes/.venv/bin/python"
                ),
                "args": [
                    os.getenv(
                        "MCP_MEETING_SERVER",
                        "/home/dd/work/diep/openhands/mcp_meeting_minutes/server.py"
                    )
                ],
                "env": {
                    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
                    "PYTHONPATH": os.getenv(
                        "MCP_MEETING_PATH",
                        "/home/dd/work/diep/openhands/mcp_meeting_minutes"
                    )
                }
            }
        
        return config if config["servers"] else None
    
    def get_system_prompt(self) -> str:
        return f"""
You are an AI assistant with access to multiple MCP tools.

Available MCP Tools:
- internet_search: Search the web (if configured)
- transcribe_audio: Transcribe audio files (if configured)
- generate_minutes: Generate meeting minutes (if configured)

Use the available tools as needed for your tasks.

{self.project_config.get_logging_rules()}
"""
    
    def get_user_prompt(self) -> str:
        return """
Demonstrate the available MCP tools.

If internet_search is available, search for something.
If other tools are available, describe what they do.
"""


def main():
    """Run the MCP example step."""
    print("\n" + "="*60)
    print("MCP Integration Example")
    print("="*60)
    print("\nAvailable examples:")
    print("1. MCPStepExample - Step with internet-search MCP")
    print("2. NoMCPStepExample - Step without MCP")
    print("3. MultiMCPStepExample - Step with multiple MCP servers")
    print("\nTo run a specific example, modify main()")
    print("="*60 + "\n")
    
    # Example: Run the MCP step
    # Uncomment one of these to run:
    
    # step = MCPStepExample()
    # step = NoMCPStepExample()
    # step = MultiMCPStepExample()
    
    # success = step.run()
    
    print("\nEdit step_example_mcp.py to run an example.")
    print("Make sure to set the required environment variables:")
    print("  - SERPER_API_KEY")
    print("  - VOYAGE_API_KEY")
    print("  - OPENAI_API_KEY (optional, for meeting minutes)")
    
    return True


if __name__ == "__main__":
    main()
