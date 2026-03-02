#!/usr/bin/env python3
"""
Test script for MCP Meeting Transcription Server
"""

import asyncio
import json
import tempfile
import os
from pathlib import Path

# Import MCP client components
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_server():
    """Test the MCP server with a simple audio file"""
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=[str(Path(__file__).parent / "server.py")],
        cwd=str(Path(__file__).parent),
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                # List available tools
                tools = await session.list_tools()
                print("Available tools:")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test with a non-existent file to see error handling
                print("\nTesting error handling with non-existent file...")
                try:
                    result = await session.call_tool(
                        "transcribe_meeting",
                        arguments={"file_path": "/non/existent/file.mp3"}
                    )
                    print("Result:", result.content[0].text)
                except Exception as e:
                    print(f"Expected error: {e}")
                
                print("\nServer test completed successfully!")
                
    except Exception as e:
        print(f"Error testing server: {e}")

if __name__ == "__main__":
    asyncio.run(test_server())