#!/usr/bin/env python3
"""
MCP Server cho xử lý âm thanh cuộc họp bằng Gemini Multimodal Live API
Hỗ trợ transcription và speaker diarization cho tiếng Việt
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import google.genai as genai
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ServerCapabilities,
    ToolsCapability,
)
from pydub import AudioSegment
from pydub.utils import make_chunks

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Khởi tạo MCP Server
server = Server("meeting-transcriber")

# Cấu hình Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY không được tìm thấy trong file .env")
    sys.exit(1)

# System instruction cho model
SYSTEM_INSTRUCTION = """Bạn là một chuyên gia gỡ băng tiếng Việt. Hãy nhận diện chính xác các từ lóng, thuật ngữ kỹ thuật và phân biệt các người nói dựa trên sắc thái giọng nói. 

Nhiệm vụ của bạn:
1. Transcribe chính xác nội dung tiếng Việt từ audio
2. Phân biệt các người nói khác nhau (Speaker Diarization)
3. Nhận diện thuật ngữ kỹ thuật, từ lóng, tên riêng
4. Trả về kết quả dưới dạng JSON với format:
{
    "full_transcript": "Nội dung đầy đủ của cuộc họp",
    "speakers": [
        {
            "speaker_id": "Speaker_1",
            "segments": [
                {
                    "start_time": "00:00:00",
                    "end_time": "00:00:10", 
                    "text": "Nội dung người nói"
                }
            ]
        }
    ]
}
"""


class AudioProcessor:
    """Xử lý audio và streaming tới Gemini Live API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        
    async def initialize_client(self):
        """Khởi tạo Gemini client"""
        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info("Đã khởi tạo Gemini client thành công")
        except Exception as e:
            logger.error(f"Lỗi khởi tạo Gemini client: {e}")
            raise
    
    def prepare_audio(self, file_path: str) -> AudioSegment:
        """Chuẩn bị audio cho streaming"""
        try:
            # Load audio file
            audio = AudioSegment.from_file(file_path)
            
            # Chuyển đổi về định dạng tối ưu cho Gemini Live API
            # PCM 16-bit, 16kHz, mono
            audio = audio.set_frame_rate(16000)
            audio = audio.set_channels(1)
            audio = audio.set_sample_width(2)  # 16-bit
            
            logger.info(f"Đã chuẩn bị audio: {len(audio)}ms, {audio.frame_rate}Hz, {audio.channels} channel(s)")
            return audio
            
        except Exception as e:
            logger.error(f"Lỗi chuẩn bị audio: {e}")
            raise
    
    async def transcribe_with_live_api(self, file_path: str) -> Dict[str, Any]:
        """Transcribe audio sử dụng Gemini API với audio input"""
        try:
            if not self.client:
                await self.initialize_client()
            
            # Chuẩn bị audio
            audio = self.prepare_audio(file_path)
            
            # Xuất audio ra file tạm thời với định dạng WAV
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                audio.export(temp_file.name, format="wav")
                temp_audio_path = temp_file.name
            
            try:
                # Upload file audio
                uploaded_file = self.client.files.upload(
                    file=temp_audio_path
                )
                
                logger.info(f"Đã upload file audio: {uploaded_file.name}")
                
                # Tạo prompt cho transcription
                prompt = f"""
                {SYSTEM_INSTRUCTION}
                
                Hãy transcribe file audio này và phân tích speaker diarization. 
                Trả về kết quả dưới dạng JSON với format chính xác như sau:
                {{
                    "full_transcript": "Nội dung đầy đủ của cuộc họp",
                    "speakers": [
                        {{
                            "speaker_id": "Speaker_1",
                            "segments": [
                                {{
                                    "start_time": "00:00:00",
                                    "end_time": "00:00:10",
                                    "text": "Nội dung người nói"
                                }}
                            ]
                        }}
                    ]
                }}
                """
                
                # Gọi Gemini API
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        prompt,
                        uploaded_file
                    ]
                )
                
                response_text = response.text
                logger.info("Đã nhận được response từ Gemini API")
                
                # Parse JSON response
                try:
                    # Tìm JSON trong response
                    import re
                    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                    else:
                        # Nếu không tìm thấy JSON, tạo response mặc định
                        result = {
                            "full_transcript": response_text,
                            "speakers": []
                        }
                    return result
                except json.JSONDecodeError:
                    # Nếu không parse được JSON, trả về text thuần
                    return {
                        "full_transcript": response_text,
                        "speakers": []
                    }
                    
            finally:
                # Xóa file tạm thời
                import os
                try:
                    os.unlink(temp_audio_path)
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Lỗi trong quá trình transcribe: {e}")
            raise


# Khởi tạo audio processor
audio_processor = AudioProcessor(GEMINI_API_KEY)


@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """Liệt kê các tools có sẵn"""
    return ListToolsResult(
        tools=[
            Tool(
                name="transcribe_meeting_native",
                description="Transcribe file âm thanh cuộc họp sử dụng Gemini Multimodal Live API với hỗ trợ speaker diarization cho tiếng Việt",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Đường dẫn tuyệt đối đến file âm thanh cần transcribe"
                        }
                    },
                    "required": ["file_path"]
                }
            )
        ]
    )


@server.call_tool()
async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
    """Xử lý các tool calls"""
    
    if request.name == "transcribe_meeting_native":
        try:
            # Lấy file path từ arguments
            file_path = request.arguments.get("file_path")
            if not file_path:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text="Lỗi: Thiếu tham số file_path"
                    )],
                    isError=True
                )
            
            # Kiểm tra file tồn tại
            if not Path(file_path).exists():
                return CallToolResult(
                    content=[TextContent(
                        type="text", 
                        text=f"Lỗi: File không tồn tại: {file_path}"
                    )],
                    isError=True
                )
            
            logger.info(f"Bắt đầu transcribe file: {file_path}")
            
            # Thực hiện transcription
            result = await audio_processor.transcribe_with_live_api(file_path)
            
            # Trả về kết quả
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )]
            )
            
        except Exception as e:
            logger.error(f"Lỗi trong transcribe_meeting_native: {e}")
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Lỗi: {str(e)}"
                )],
                isError=True
            )
    
    else:
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"Tool không được hỗ trợ: {request.name}"
            )],
            isError=True
        )


async def main():
    """Chạy MCP server"""
    # Khởi tạo audio processor
    try:
        await audio_processor.initialize_client()
        logger.info("MCP Server đã sẵn sàng")
    except Exception as e:
        logger.error(f"Lỗi khởi tạo: {e}")
        sys.exit(1)
    
    # Chạy server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="meeting-transcriber",
                server_version="1.0.0",
                capabilities=ServerCapabilities(
                    tools=ToolsCapability(listChanged=False)
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())