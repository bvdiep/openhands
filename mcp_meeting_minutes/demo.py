#!/usr/bin/env python3
"""
Demo script for MCP Meeting Transcription Server
"""

import asyncio
import json
import os
from pathlib import Path

# Import MCP client components
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def demo_transcription():
    """Demo the MCP server with a test audio file"""
    
    # Get absolute path to test audio file
    test_audio_path = str(Path(__file__).parent / "test_audio.wav")
    
    if not os.path.exists(test_audio_path):
        print(f"Test audio file not found: {test_audio_path}")
        print("Please run the server creation script first to generate test_audio.wav")
        return
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=[str(Path(__file__).parent / "server.py")],
        cwd=str(Path(__file__).parent),
    )
    
    try:
        print("🎵 Starting MCP Meeting Transcription Demo...")
        print(f"📁 Test audio file: {test_audio_path}")
        print(f"📊 File size: {os.path.getsize(test_audio_path)} bytes")
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                # List available tools
                tools = await session.list_tools()
                print(f"\n🔧 Available tools: {len(tools.tools)}")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test transcription with the test audio file
                print(f"\n🎙️  Starting transcription of {test_audio_path}...")
                print("⏳ This may take a moment...")
                
                try:
                    result = await session.call_tool(
                        "transcribe_meeting",
                        arguments={"file_path": test_audio_path}
                    )
                    
                    # Parse the result
                    result_data = json.loads(result.content[0].text)
                    
                    print("\n✅ Transcription completed!")
                    print("📋 Results:")
                    print(f"  - Duration: {result_data['duration_seconds']:.2f} seconds")
                    print(f"  - Format: {result_data['file_info']['format']}")
                    print(f"  - Size: {result_data['file_info']['size_mb']} MB")
                    print(f"  - Chunks processed: {result_data['file_info']['chunks_processed']}")
                    print(f"  - Transcript: '{result_data['full_transcript']}'")
                    
                    if result_data['full_transcript'].strip():
                        print("\n🎉 Success! The server successfully processed the audio file.")
                    else:
                        print("\n⚠️  Note: The test audio file is just a tone, so no speech was detected.")
                        print("   Try with a real audio file containing speech for actual transcription.")
                    
                except Exception as e:
                    print(f"❌ Error during transcription: {e}")
                
                print("\n🏁 Demo completed!")
                
    except Exception as e:
        print(f"❌ Error running demo: {e}")

if __name__ == "__main__":
    asyncio.run(demo_transcription())