# MCP Meeting Minutes Repository

## Overview
This repository contains a Model Context Protocol (MCP) Server for transcribing meeting audio files using Groq API with smart chunking capabilities.

## Key Components

### 1. Core Server (`server.py`)
- **MCP Server**: Implements MCP protocol for audio transcription
- **Smart Chunking**: Automatically splits large files (>25MB) into 10-minute chunks
- **Audio Processing**: Supports multiple formats (.ogg, .mp3, .wav, .m4a, .flac, .aac)
- **Groq Integration**: Uses whisper-large-v3 model for high-quality transcription
- **Error Handling**: Comprehensive error handling for file issues and API limits
- **Async Processing**: Non-blocking operations to prevent server hanging

### 2. Audio Processor Class
- **Format Detection**: Automatic audio format detection
- **File Size Management**: Handles large files with intelligent chunking
- **Duration Calculation**: Uses librosa with pydub fallback
- **Temporary File Management**: Automatic cleanup of chunk files
- **Transcription Pipeline**: Manages API calls and result stitching

### 3. Configuration & Setup
- **Environment Variables**: Secure API key management via .env
- **Virtual Environment**: Isolated Python environment (.venv)
- **Dependencies**: All required packages in requirements.txt
- **FFmpeg Integration**: Required for audio processing

## Architecture Patterns

### MCP Protocol Implementation
- **Tool Registration**: `@server.list_tools()` decorator
- **Tool Execution**: `@server.call_tool()` with proper signature
- **Error Handling**: Graceful error responses in JSON format
- **Async Operations**: Full async/await support

### Audio Processing Pipeline
1. **Validation**: File existence and format checking
2. **Analysis**: Size and duration calculation
3. **Chunking**: Smart splitting for large files
4. **Transcription**: Parallel processing of chunks
5. **Stitching**: Combining results in correct order
6. **Cleanup**: Automatic temporary file removal

## Integration Points

### Claude Desktop
- Configuration via `claude_desktop_config.json`
- Absolute paths required for proper execution
- Environment variable passing for API keys

### Telegram Bot Backend
- MCP client integration example provided
- Async session management
- File download and processing workflow

## Testing & Validation

### Test Scripts
- `test_server.py`: Basic server functionality testing
- `demo.py`: Full transcription pipeline demonstration
- Error handling validation with non-existent files

### Audio File Testing
- Generated test tone for basic functionality
- Real audio file support for speech transcription
- Multiple format compatibility testing

## Performance Considerations

### File Size Optimization
- 25MB threshold for chunking decision
- 10-minute chunk duration for optimal API usage
- Memory-efficient processing with streaming

### API Rate Limiting
- Groq API integration with error handling
- Retry logic for transient failures
- Proper error reporting for rate limits

## Security & Best Practices

### API Key Management
- Environment variable storage
- .env.example template provided
- No hardcoded credentials

### File Handling
- Absolute path validation
- Temporary file cleanup
- Format validation before processing

## Known Limitations

1. **Groq API Dependency**: Requires valid API key and internet connection
2. **FFmpeg Requirement**: System dependency for audio processing
3. **File Size Limits**: Large files require chunking (may affect context)
4. **Language Support**: Limited to Groq's whisper model capabilities

## Future Enhancements

1. **Multi-language Support**: Language detection and selection
2. **Speaker Diarization**: Identify different speakers in meetings
3. **Summary Generation**: AI-powered meeting summaries
4. **Real-time Processing**: Streaming audio transcription
5. **Custom Models**: Support for other transcription services

## Troubleshooting Patterns

### Common Issues
1. **FFmpeg Missing**: Installation instructions in README
2. **API Key Issues**: Validation and error messages
3. **File Format Problems**: Comprehensive format support
4. **Memory Issues**: Chunking for large files
5. **Network Problems**: Retry logic and error handling

### Debug Strategies
- Console logging for chunk processing
- JSON error responses with context
- File validation before processing
- Environment variable checking