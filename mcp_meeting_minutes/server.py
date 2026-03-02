#!/usr/bin/env python3
"""
MCP Server for Meeting Audio Transcription
Handles audio files and transcribes them using Groq API with smart chunking
"""

import asyncio
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from groq import Groq
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.types import (
    Tool,
    TextContent,
)
from pydub import AudioSegment
import librosa

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Server instance
server = Server("meeting-transcription-server")

# Constants
MAX_FILE_SIZE_MB = 25
CHUNK_DURATION_MINUTES = 10
SUPPORTED_FORMATS = ['.ogg', '.mp3', '.wav', '.m4a', '.flac', '.aac']


class AudioProcessor:
    """Handles audio file processing and transcription"""
    
    @staticmethod
    def detect_format(file_path: str) -> str:
        """Detect audio format from file extension"""
        ext = Path(file_path).suffix.lower()
        if ext not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported audio format: {ext}. Supported formats: {SUPPORTED_FORMATS}")
        return ext[1:]  # Remove the dot
    
    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """Get file size in MB"""
        return os.path.getsize(file_path) / (1024 * 1024)
    
    @staticmethod
    def get_audio_duration(file_path: str) -> float:
        """Get audio duration in seconds using librosa"""
        try:
            duration = librosa.get_duration(path=file_path)
            return duration
        except Exception as e:
            # Fallback to pydub if librosa fails
            audio = AudioSegment.from_file(file_path)
            return len(audio) / 1000.0
    
    @staticmethod
    def chunk_audio(file_path: str, chunk_duration_minutes: int = CHUNK_DURATION_MINUTES) -> List[str]:
        """
        Split audio file into chunks if it's too large
        Returns list of temporary file paths
        """
        file_size_mb = AudioProcessor.get_file_size_mb(file_path)
        
        if file_size_mb <= MAX_FILE_SIZE_MB:
            return [file_path]
        
        # Load audio file
        audio = AudioSegment.from_file(file_path)
        chunk_length_ms = chunk_duration_minutes * 60 * 1000  # Convert to milliseconds
        
        chunks = []
        temp_files = []
        
        # Split audio into chunks
        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i + chunk_length_ms]
            chunks.append(chunk)
        
        # Save chunks to temporary files
        for i, chunk in enumerate(chunks):
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=f"_chunk_{i}.wav",
                prefix="meeting_audio_"
            )
            chunk.export(temp_file.name, format="wav")
            temp_files.append(temp_file.name)
            temp_file.close()
        
        return temp_files
    
    @staticmethod
    async def transcribe_audio_file(file_path: str) -> str:
        """Transcribe a single audio file using Groq API"""
        try:
            with open(file_path, "rb") as audio_file:
                transcription = groq_client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3",
                    response_format="text"
                )
                return transcription
        except Exception as e:
            raise Exception(f"Transcription failed for {file_path}: {str(e)}")
    
    @staticmethod
    def cleanup_temp_files(temp_files: List[str]) -> None:
        """Clean up temporary files"""
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                print(f"Warning: Could not delete temporary file {temp_file}: {e}")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="transcribe_meeting",
            description="Transcribe audio files from meetings using Groq API with smart chunking for large files",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute path to the audio file (supports .ogg, .mp3, .wav, .m4a, .flac, .aac)"
                    }
                },
                "required": ["file_path"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[TextContent]:
    """Handle tool calls"""
    
    if name != "transcribe_meeting":
        raise ValueError(f"Unknown tool: {name}")
    
    # Extract arguments
    if not arguments:
        raise ValueError("Arguments are required")
        
    file_path = arguments.get("file_path")
    if not file_path:
        raise ValueError("file_path is required")
    
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    try:
        # Detect format
        audio_format = AudioProcessor.detect_format(file_path)
        
        # Get file info
        file_size_mb = AudioProcessor.get_file_size_mb(file_path)
        duration_seconds = AudioProcessor.get_audio_duration(file_path)
        
        # Process audio (chunk if necessary)
        chunk_files = AudioProcessor.chunk_audio(file_path)
        temp_files_to_cleanup = []
        
        # Keep track of which files are temporary
        if len(chunk_files) > 1:
            temp_files_to_cleanup = chunk_files
        
        try:
            # Transcribe each chunk
            transcriptions = []
            for i, chunk_file in enumerate(chunk_files):
                print(f"Transcribing chunk {i+1}/{len(chunk_files)}: {chunk_file}")
                transcription = await AudioProcessor.transcribe_audio_file(chunk_file)
                transcriptions.append(transcription)
            
            # Combine transcriptions
            full_transcript = " ".join(transcriptions)
            
            # Prepare result
            result = {
                "full_transcript": full_transcript,
                "duration_seconds": duration_seconds,
                "file_info": {
                    "original_file": file_path,
                    "format": audio_format,
                    "size_mb": round(file_size_mb, 2),
                    "chunks_processed": len(chunk_files)
                }
            }
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, ensure_ascii=False)
                )
            ]
            
        finally:
            # Clean up temporary files
            if temp_files_to_cleanup:
                AudioProcessor.cleanup_temp_files(temp_files_to_cleanup)
    
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "error": str(e),
                    "file_path": file_path
                }, indent=2)
            )
        ]


async def main():
    """Main server function"""
    # Check if GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY not found in environment variables")
        print("Please set GROQ_API_KEY in your .env file")
        return
    
    print("Starting Meeting Transcription MCP Server...")
    print(f"Supported audio formats: {', '.join(SUPPORTED_FORMATS)}")
    print(f"Max file size before chunking: {MAX_FILE_SIZE_MB}MB")
    print(f"Chunk duration: {CHUNK_DURATION_MINUTES} minutes")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="meeting-transcription-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())