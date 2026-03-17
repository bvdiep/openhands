"""
Step 02: Screenshot Worker Implementation

This step creates the main screenshot worker that can capture screenshots
of URLs protected by basic authentication using Cloudflare Browser Rendering API.
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from base_step import BaseStep


class ScreenshotWorkerStep(BaseStep):
    """
    Step 02: Implement the screenshot worker with basic authentication support.
    
    This step will:
    1. Create the screenshot worker TypeScript code
    2. Configure wrangler.toml for the worker
    3. Implement basic authentication handling
    4. Set up Cloudflare Browser Rendering integration
    """

    def __init__(self):
        super().__init__(
            step_name="Screenshot Worker Implementation",
            step_number=2
        )

   #  def get_model(self) -> str:
   #      return "openai/kimi-2.5"
    
    def get_system_prompt(self) -> str:
        return f"""
You are an expert Cloudflare Workers developer specializing in browser automation and screenshot services.

CRITICAL DOCUMENTATION:
- Cloudflare Browser Rendering API: https://developers.cloudflare.com/browser-rendering/
- Browser Rendering Examples: https://developers.cloudflare.com/browser-rendering/examples/
- Workers Runtime API: https://developers.cloudflare.com/workers/runtime-apis/

TECHNICAL REQUIREMENTS:
1. **Screenshot Worker Features**:
   - Accept URL parameter via query string or POST body
   - Support basic authentication (username/password)
   - Use Cloudflare Browser Rendering API for screenshots
   - Return screenshot as image response
   - Handle errors gracefully
   - Support different image formats (PNG, JPEG)
   - Optional viewport size configuration

2. **Basic Authentication Handling**:
   - Accept auth credentials via request headers or body
   - Properly encode credentials for HTTP Basic Auth
   - Handle both protected and unprotected URLs
   - Secure credential handling

3. **Cloudflare Browser Rendering Integration**:
   - Use the Browser Rendering API correctly
   - Handle browser session management
   - Implement proper error handling
   - Optimize for performance and cost

4. **Worker Configuration**:
   - Proper wrangler.toml configuration
   - Environment variables for sensitive data
   - Appropriate resource limits
   - CORS headers if needed

IMPLEMENTATION GUIDELINES:
- Use TypeScript with proper type definitions
- Implement comprehensive error handling
- Add request validation
- Use environment variables for configuration
- Follow Cloudflare Workers best practices
- Add proper logging for debugging

SECURITY CONSIDERATIONS:
- Never log sensitive credentials
- Validate all input parameters
- Implement rate limiting if needed
- Use secure headers

{self.project_config.get_logging_rules()}
"""
    
    def get_user_prompt(self) -> str:
        return f"""
Implement the screenshot worker for capturing screenshots of URLs with basic authentication support.

PROJECT CONTEXT:
- Project: {self.project_config.project_name}
- Workspace: {self.project_config.workspace_path}
- Worker Location: screenshot-web/

STEP 2 REQUIREMENTS:

1. **Create screenshot-web/src/index.ts**:
   Implement a Cloudflare Worker with the following features:
   
   **API Endpoints**:
   - GET /screenshot?url=<URL>&username=<USER>&password=<PASS>
   - POST /screenshot with JSON body: {{"url": "...", "username": "...", "password": "...", "options": {{...}}}}
   
   **Core Features**:
   - Use Cloudflare Browser Rendering API to capture screenshots
   - Handle basic authentication for protected URLs
   - Support optional parameters:
     - viewport: width/height (default: 1920x1080)
     - format: png/jpeg (default: png)
     - quality: 1-100 for JPEG (default: 90)
     - fullPage: boolean (default: false)
   - Return screenshot as image response with proper headers
   - Comprehensive error handling and validation
   
   **Security & Performance**:
   - Input validation for all parameters
   - Proper error messages without exposing sensitive data
   - CORS headers for web usage
   - Request timeout handling

2. **Create screenshot-web/wrangler.toml**:
   Configure the worker with:
   - Worker name: "screenshot-web"
   - Compatibility date and flags
   - Browser Rendering binding
   - Environment variables setup
   - Resource limits appropriate for browser rendering

3. **TypeScript Types**:
   Create proper TypeScript interfaces for:
   - Request/response types
   - Configuration options
   - Error handling
   - Browser Rendering API types

4. **Implementation Details**:
   
   **Basic Auth Implementation**:
   ```typescript
   // Handle basic authentication
   const authHeader = btoa(`${{username}}:${{password}}`);
   await page.setExtraHTTPHeaders({{
     'Authorization': `Basic ${{authHeader}}`
   }});
   ```
   
   **Browser Rendering Usage**:
   ```typescript
   // Use the Browser Rendering API
   const browser = await puppeteer.launch(env.BROWSER);
   const page = await browser.newPage();
   // ... screenshot logic
   ```

5. **Error Handling**:
   - Invalid URL format
   - Authentication failures
   - Timeout errors
   - Browser rendering failures
   - Network connectivity issues

EXAMPLE USAGE:
```bash
# Basic screenshot
curl "https://your-worker.your-subdomain.workers.dev/screenshot?url=https://example.com"

# With basic auth
curl "https://your-worker.your-subdomain.workers.dev/screenshot?url=https://protected.example.com&username=user&password=pass"

# POST with options
curl -X POST "https://your-worker.your-subdomain.workers.dev/screenshot" \\
  -H "Content-Type: application/json" \\
  -d '{{"url": "https://example.com", "options": {{"viewport": {{"width": 1280, "height": 720}}, "format": "jpeg"}}}}'
```

REFERENCE DOCUMENTATION:
Use the Cloudflare Browser Rendering documentation at https://developers.cloudflare.com/browser-rendering/ for:
- API usage examples
- Configuration options
- Best practices
- Error handling patterns

Log all implementation details to: {self.project_config.log_full_path}

Focus on creating a production-ready worker that handles edge cases gracefully.
"""


def main():
    """Run the Screenshot Worker Implementation step."""
    step = ScreenshotWorkerStep()
    success = step.run()
    return success


if __name__ == "__main__":
    main()