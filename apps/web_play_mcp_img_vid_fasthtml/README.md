# MCP FastHTML UI

A FastHTML web application to manage and execute MCP tools.

## Setup

1. Install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8100
   ```
   Or using PM2:
   ```bash
   pm2 start ecosystem.config.json
   ```

## Features
- Dynamic form generation based on MCP tool schema
- File upload support for image/video parameters
- Gallery view for generated outputs
- HTMX-powered seamless UI updates
