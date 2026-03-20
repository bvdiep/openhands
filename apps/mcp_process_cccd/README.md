# MCP Process CCCD

## 1. Overview
The MCP Process CCCD server is a Model Context Protocol (MCP) server designed to process and handle CCCD (Citizen Identity Card) operations. It integrates with a backend web application to upload, analyze, and extract information from CCCD images using Gemini and browser automation via Playwright.

## 2. Setup and Installation

To set up the server, install the required Python dependencies and the Playwright browsers:

```bash
# Install Python requirements
pip install -r requirements.txt

# Install Playwright browsers (required for browser automation)
playwright install
```

## 3. Configuration

Create a `.env` file in the `apps/mcp_process_cccd/` directory by copying the provided example:

```bash
cp .env.example .env
```

Configure the following environment variables in your `.env` file:

- `APP_URL`: The URL of the target web application (e.g., `http://127.0.0.1:5005`).
- `ADMIN_USERNAME`: The admin username for logging into the web application.
- `ADMIN_PASSWORD`: The admin password for logging into the web application.
- `GEMINI_API_KEY`: Your Google Gemini API key used for AI-based extraction and processing.
- `GEMINI_MODEL`: The Gemini model to use (default is `gemini-3-flash-preview`).
- `HEADLESS`: Set to `true` to run the Playwright browser in headless mode, or `false` to see the browser UI during execution.

## 4. How to Start the Server

You can start the server directly using Python or via the MCP CLI for development:

**For Development (using MCP CLI):**
```bash
mcp dev mcp_server.py
```
*Note: This runs the server with the MCP inspector to help you debug tools and resources.*

**Direct Execution:**
```bash
python mcp_server.py
```

## 5. Claude Desktop Configuration

To use this MCP server with Claude Desktop, you need to add it to your Claude Desktop configuration file (`claude_desktop_config.json`).

Add the following configuration under the `mcpServers` object, replacing `/absolute/path/to/openhands/apps/mcp_process_cccd` with the actual absolute path to the directory on your system:

```json
{
  "mcpServers": {
    "mcp-process-cccd": {
      "command": "python",
      "args": [
        "/absolute/path/to/openhands/apps/mcp_process_cccd/mcp_server.py"
      ],
      "env": {
        "APP_URL": "http://127.0.0.1:5005",
        "ADMIN_USERNAME": "admin",
        "ADMIN_PASSWORD": "secret",
        "GEMINI_API_KEY": "your_api_key_here",
        "GEMINI_MODEL": "gemini-3-flash-preview",
        "HEADLESS": "true"
      }
    }
  }
}
```
*Tip: Ensure that you are using the correct Python executable path if you are using a virtual environment (e.g., `/path/to/venv/bin/python`).*
