# Kế hoạch Tích hợp MCP vào BaseStep

## 📋 Tổng quan

Tài liệu này mô tả kế hoạch chi tiết để tích hợp Model Context Protocol (MCP) vào [`openhands_v2/base_step.py`](../openhands_v2/base_step.py), cho phép mỗi step có thể sử dụng MCP servers như internet-search.

## 🎯 Mục tiêu

Bổ sung khả năng MCP vào [`BaseStep`](../openhands_v2/base_step.py) để:
- Mỗi step có thể định nghĩa MCP servers riêng
- Tích hợp MCP servers như một phần của agent configuration
- Hỗ trợ nhiều loại MCP transport (stdio, SSE, HTTP)
- Duy trì backward compatibility với code hiện tại

## 🔍 Phân tích Hiện tại

### Cấu trúc BaseStep hiện tại

```python
class BaseStep(ABC):
    def __init__(self, step_name: str, step_number: int, model: Optional[str] = None)
    
    # Abstract methods
    def get_system_prompt(self) -> str
    def get_user_prompt(self) -> str
    
    # Overridable methods
    def get_tools(self) -> List[Tool]
    def get_model(self) -> Optional[str]
    
    # Setup methods
    def setup_llm(self) -> LLM
    def setup_agent(self) -> Agent
    def setup_conversation(self) -> Conversation
    
    # Execution
    def run(self) -> bool
```

### OpenHands SDK Agent với MCP

Theo tài liệu OpenHands SDK, Agent hỗ trợ `mcp_config` parameter:

```python
from openhands.sdk import Agent

agent = Agent(
    llm=llm,
    tools=[...],
    system_prompt="...",
    mcp_config={
        "servers": {
            "server-name": {
                "type": "stdio",  # hoặc "sse", "http"
                "command": "/path/to/python",
                "args": ["/path/to/server.py"],
                "env": {...}
            }
        }
    }
)
```

## 🏗️ Thiết kế Giải pháp

### 1. Thêm method `get_mcp_config()` vào BaseStep

```python
def get_mcp_config(self) -> Optional[Dict[str, Any]]:
    """
    Return MCP configuration for this step.
    Can be overridden if a step needs MCP servers.
    
    Returns:
        dict: MCP configuration with servers
        None: No MCP servers needed (default)
    
    Example:
        def get_mcp_config(self) -> Dict[str, Any]:
            return {
                "servers": {
                    "internet-search": {
                        "type": "stdio",
                        "command": "/path/to/python",
                        "args": ["/path/to/server.py"],
                        "env": {
                            "SERPER_API_KEY": "...",
                            "VOYAGE_API_KEY": "..."
                        }
                    }
                }
            }
    """
    return None  # Default: no MCP servers
```

### 2. Cập nhật `setup_agent()` để sử dụng MCP config

```python
def setup_agent(self) -> Agent:
    """Initialize and return Agent instance with MCP support."""
    if not self.llm:
        self.setup_llm()
    
    # Get MCP config if available
    mcp_config = self.get_mcp_config()
    
    # Create agent with or without MCP
    if mcp_config:
        self.agent = Agent(
            llm=self.llm,
            tools=self.get_tools(),
            system_prompt=self.get_system_prompt(),
            mcp_config=mcp_config
        )
    else:
        self.agent = Agent(
            llm=self.llm,
            tools=self.get_tools(),
            system_prompt=self.get_system_prompt()
        )
    
    return self.agent
```

### 3. Cấu trúc MCP Configuration

#### Stdio MCP Server (Local)
```python
{
    "servers": {
        "internet-search": {
            "type": "stdio",
            "command": "/home/dd/work/diep/openhands/mcp_internet/.venv/bin/python",
            "args": ["/home/dd/work/diep/openhands/mcp_internet/server.py"],
            "env": {
                "SERPER_API_KEY": os.getenv("SERPER_API_KEY", "YOUR_SERPER_API_KEY"),
                "VOYAGE_API_KEY": os.getenv("VOYAGE_API_KEY", "YOUR_VOYAGE_API_KEY"),
                "PYTHONPATH": "/home/dd/work/diep/openhands/mcp_internet"
            }
        }
    }
}
```

#### SSE MCP Server (Remote)
```python
{
    "servers": {
        "remote-service": {
            "type": "sse",
            "url": "http://localhost:3000/sse",
            "headers": {
                "Authorization": "Bearer YOUR_API_KEY"
            }
        }
    }
}
```

#### HTTP MCP Server
```python
{
    "servers": {
        "http-service": {
            "type": "http",
            "url": "http://localhost:3000/mcp"
        }
    }
}
```

## 📝 Ví dụ Sử dụng

### Ví dụ 1: Step với Internet Search MCP

```python
"""
Step 01: Research with Internet Search
"""
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class ResearchStep(BaseStep):
    """Step 01: Research using internet search."""
    
    def __init__(self):
        super().__init__(
            step_name="Research & Analysis",
            step_number=1
        )
    
    def get_mcp_config(self):
        """Configure internet search MCP server."""
        return {
            "servers": {
                "internet-search": {
                    "type": "stdio",
                    "command": "/home/dd/work/diep/openhands/mcp_internet/.venv/bin/python",
                    "args": ["/home/dd/work/diep/openhands/mcp_internet/server.py"],
                    "env": {
                        "SERPER_API_KEY": os.getenv("SERPER_API_KEY", "YOUR_SERPER_API_KEY"),
                        "VOYAGE_API_KEY": os.getenv("VOYAGE_API_KEY", "YOUR_VOYAGE_API_KEY"),
                        "PYTHONPATH": "/home/dd/work/diep/openhands/mcp_internet"
                    }
                }
            }
        }
    
    def get_system_prompt(self) -> str:
        return """
You are a research expert with access to internet search capabilities.

Use the 'internet_search' tool to find relevant information online.
The tool will:
1. Search using Serper API
2. Rerank results using VoyageAI
3. Crawl and extract clean content

Always cite your sources and provide accurate information.
"""
    
    def get_user_prompt(self) -> str:
        return """
Research the latest trends in AI agent development.
Focus on:
1. Model Context Protocol (MCP)
2. Agent frameworks
3. Tool integration patterns

Provide a comprehensive summary with sources.
"""


def main():
    """Run Step 01."""
    step = ResearchStep()
    success = step.run()
    
    if success:
        print("\n✓ Step 01 hoàn tất.")
    else:
        print("\n✗ Step 01 thất bại.")
    
    return success


if __name__ == "__main__":
    main()
```

### Ví dụ 2: Step không dùng MCP (Default)

```python
"""
Step 02: Implementation without MCP
"""
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class ImplementationStep(BaseStep):
    """Step 02: Implementation using default tools only."""
    
    def __init__(self):
        super().__init__(
            step_name="Implementation",
            step_number=2
        )
    
    # Không override get_mcp_config() -> không dùng MCP
    
    def get_system_prompt(self) -> str:
        return "You are a coding expert..."
    
    def get_user_prompt(self) -> str:
        return "Implement the features..."
```

### Ví dụ 3: Step với nhiều MCP servers

```python
"""
Step 03: Multi-MCP Step
"""
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class MultiMCPStep(BaseStep):
    """Step 03: Using multiple MCP servers."""
    
    def __init__(self):
        super().__init__(
            step_name="Multi-MCP Analysis",
            step_number=3
        )
    
    def get_mcp_config(self):
        """Configure multiple MCP servers."""
        return {
            "servers": {
                "internet-search": {
                    "type": "stdio",
                    "command": "/home/dd/work/diep/openhands/mcp_internet/.venv/bin/python",
                    "args": ["/home/dd/work/diep/openhands/mcp_internet/server.py"],
                    "env": {
                        "SERPER_API_KEY": "...",
                        "VOYAGE_API_KEY": "..."
                    }
                },
                "meeting-minutes": {
                    "type": "stdio",
                    "command": "/home/dd/work/diep/openhands/mcp_meeting_minutes/.venv/bin/python",
                    "args": ["/home/dd/work/diep/openhands/mcp_meeting_minutes/server.py"],
                    "env": {
                        "OPENAI_API_KEY": "..."
                    }
                }
            }
        }
    
    def get_system_prompt(self) -> str:
        return """
You have access to multiple tools:
- internet_search: Search and analyze web content
- transcribe_audio: Transcribe meeting audio
- generate_minutes: Generate meeting minutes

Use these tools as needed for your tasks.
"""
    
    def get_user_prompt(self) -> str:
        return "Analyze the meeting and research related topics..."
```

## 🔧 Cấu hình MCP từ Environment Variables

Để bảo mật API keys, nên load từ environment variables:

```python
import os

def get_mcp_config(self):
    """Configure MCP with environment variables."""
    return {
        "servers": {
            "internet-search": {
                "type": "stdio",
                "command": os.getenv("MCP_INTERNET_PYTHON", 
                    "/home/dd/work/diep/openhands/mcp_internet/.venv/bin/python"),
                "args": [os.getenv("MCP_INTERNET_SERVER",
                    "/home/dd/work/diep/openhands/mcp_internet/server.py")],
                "env": {
                    "SERPER_API_KEY": os.getenv("SERPER_API_KEY"),
                    "VOYAGE_API_KEY": os.getenv("VOYAGE_API_KEY"),
                    "PYTHONPATH": os.getenv("MCP_INTERNET_PATH",
                        "/home/dd/work/diep/openhands/mcp_internet")
                }
            }
        }
    }
```

## 🎯 Lợi ích của Thiết kế

### 1. Flexibility
- Mỗi step có thể định nghĩa MCP servers riêng
- Hỗ trợ nhiều loại MCP transport
- Dễ dàng thêm/bớt MCP servers

### 2. Backward Compatibility
- Steps không dùng MCP vẫn hoạt động bình thường
- Không cần thay đổi code hiện tại
- Default behavior: không có MCP

### 3. Consistent Pattern
- Theo pattern của `get_tools()` và `get_model()`
- Dễ hiểu và sử dụng
- Tài liệu rõ ràng

### 4. Security
- API keys có thể load từ environment variables
- Không hardcode sensitive data
- Dễ dàng quản lý credentials

### 5. Maintainability
- Code rõ ràng, dễ maintain
- Dễ dàng debug và test
- Tách biệt concerns

## 📊 So sánh với các Phương án khác

### Phương án 1: MCP trong ProjectConfig (Rejected)
```python
# ❌ Không linh hoạt - tất cả steps dùng chung MCP
project_config = ProjectConfig(
    project_name="my-project",
    mcp_servers={...}
)
```

**Nhược điểm:**
- Không linh hoạt cho từng step
- Khó quản lý khi steps cần MCP khác nhau
- Tăng complexity của ProjectConfig

### Phương án 2: MCP trong LLM_CONFIG (Rejected)
```python
# ❌ Global config - không phù hợp
LLM_CONFIG = {
    "model": "...",
    "mcp_servers": {...}
}
```

**Nhược điểm:**
- Global scope không phù hợp
- Không thể customize per-step
- Khó test và debug

### Phương án 3: MCP trong get_mcp_config() (✅ Recommended)
```python
# ✅ Linh hoạt, rõ ràng, dễ maintain
def get_mcp_config(self):
    return {
        "servers": {...}
    }
```

**Ưu điểm:**
- Linh hoạt cho từng step
- Consistent với pattern hiện tại
- Dễ override và customize
- Backward compatible

## 🚀 Roadmap Triển khai

### Phase 1: Core Implementation ✅
- [x] Phân tích cấu trúc hiện tại
- [x] Nghiên cứu OpenHands SDK MCP support
- [x] Thiết kế cấu trúc MCP configuration
- [ ] Implement `get_mcp_config()` method
- [ ] Cập nhật `setup_agent()` method

### Phase 2: Examples & Documentation
- [ ] Tạo ví dụ step với internet-search MCP
- [ ] Tạo ví dụ step với multiple MCP servers
- [ ] Viết tài liệu hướng dẫn sử dụng
- [ ] Cập nhật README.md

### Phase 3: Testing & Validation
- [ ] Test với MCP internet-search có sẵn
- [ ] Test với MCP meeting-minutes
- [ ] Test backward compatibility
- [ ] Test error handling

### Phase 4: Advanced Features (Future)
- [ ] MCP server health check
- [ ] MCP server auto-discovery
- [ ] MCP server pooling
- [ ] MCP server monitoring

## 📚 Tài liệu Tham khảo

1. **OpenHands SDK Documentation**
   - [MCP Guide](https://docs.openhands.dev/sdk/guides/mcp)
   - [Agent API Reference](https://docs.openhands.dev/sdk/api-reference/openhands.sdk.agent)

2. **Model Context Protocol**
   - [Official MCP Specification](https://modelcontextprotocol.io)
   - [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

3. **OpenHands MCP Settings**
   - [MCP Configuration](https://docs.openhands.dev/openhands/usage/settings/mcp-settings)

## 🔍 Best Practices

### 1. API Key Management
```python
# ✅ Good: Load from environment
"SERPER_API_KEY": os.getenv("SERPER_API_KEY")

# ❌ Bad: Hardcode in code
"SERPER_API_KEY": os.getenv("SERPER_API_KEY", "YOUR_SERPER_API_KEY")
```

### 2. Path Configuration
```python
# ✅ Good: Use absolute paths or environment variables
"command": os.path.join(os.getcwd(), "mcp_internet/.venv/bin/python")

# ❌ Bad: Hardcode absolute paths
"command": "/home/dd/work/diep/openhands/mcp_internet/.venv/bin/python"
```

### 3. Error Handling
```python
def get_mcp_config(self):
    """Configure MCP with error handling."""
    try:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            print("Warning: SERPER_API_KEY not set, MCP disabled")
            return None
        
        return {
            "servers": {
                "internet-search": {...}
            }
        }
    except Exception as e:
        print(f"Error configuring MCP: {e}")
        return None
```

### 4. Documentation
```python
def get_mcp_config(self):
    """
    Configure MCP servers for this step.
    
    This step uses internet-search MCP server for web research.
    
    Required environment variables:
    - SERPER_API_KEY: API key for Serper search
    - VOYAGE_API_KEY: API key for VoyageAI reranking
    
    Returns:
        dict: MCP configuration with servers
        None: If environment variables not set
    """
    # Implementation...
```

## 🎓 Kết luận

Thiết kế này cung cấp một cách linh hoạt và mạnh mẽ để tích hợp MCP vào BaseStep:

1. **Simple**: Chỉ cần override `get_mcp_config()` khi cần
2. **Flexible**: Mỗi step có thể có MCP servers riêng
3. **Consistent**: Theo pattern hiện tại của BaseStep
4. **Backward Compatible**: Không ảnh hưởng code hiện tại
5. **Secure**: Hỗ trợ environment variables cho API keys
6. **Maintainable**: Code rõ ràng, dễ maintain

Thiết kế này sẽ cho phép bạn dễ dàng sử dụng MCP internet-search và các MCP servers khác trong bất kỳ step nào của pipeline.
