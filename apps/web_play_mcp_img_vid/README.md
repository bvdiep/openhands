# MCP Media Generator Web UI

This is a Streamlit web interface for controlling the MCP tools for generating media (Image/Video) using Google's Gemini and Veo models.

## Setup

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Ensure the MCP server is set up at `/home/dd/work/diep/openhands/apps/mcp_gen_img_vid_with_refs` with its own virtual environment and `.env` file containing the necessary API keys.

## Running the App

Run the Streamlit app with the following command:

```bash
streamlit run app.py --server.headless true
```

## Features

- **Generate Custom Scene Image**: Upload reference images (faces, background, pose, items) and provide a prompt to generate a new scene.
- **Generate Video from Scene Image**: Upload a context image and provide a prompt to generate a video.
- **Output Gallery**: View and preview previously generated images and videos, sorted by newest first.
- **Debug Logs**: Expandable section to view the raw JSON output and debug information from the MCP tool execution.
