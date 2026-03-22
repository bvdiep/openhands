# MCP Gen Image with Face Reference

This Model Context Protocol (MCP) server provides tools for generating custom scene images with references (such as face, background, pose, or item) and generating videos from those scene images using Google's Gemini and Veo models.

## Features

- **Custom Scene Image Generation**: Uses the `gemini-3.1-flash-image-preview` model to generate scene images incorporating specific references like faces, backgrounds, poses, or items.
- **Video Generation**: Uses the `veo-3.0-generate-001` model to generate videos from scene images, supporting both horizontal and vertical orientations.

## Prerequisites

- Python 3.10+
- `uv` package manager (recommended)
- Google Gemini API Key

## Environment Variables

The server requires the following environment variables to function correctly:

- `GEMINI_API_KEY`: Your Google Gemini API key. This is required as the server uses `genai.Client()` to interact with the models.

You can set this in a `.env` file in the root of the app directory. Copy the `.env.example` file to `.env` and fill in your API key:

```bash
cp .env.example .env
```

## Tools

This MCP server provides the following tools:

### `generate_custom_scene_image`

Generates a custom scene image based on a prompt and optional reference images.

**Model:** `gemini-3.1-flash-image-preview`

**Parameters:**
- `prompt` (string): The description of the scene you want to generate.
- `face_reference_paths` (array of strings, optional): List of paths to reference images containing faces.
- `background_reference_path` (string, optional): Path to a reference image for the background/scene.
- `pose_reference_path` (string, optional): Path to a reference image for the character's pose.
- `item_reference_paths` (array of strings, optional): List of paths to reference images for specific items to include.

### `generate_video_from_scene_image`

Generates a video from an existing scene image.

**Model:** `veo-3.0-generate-001`

**Parameters:**
- `image_path` (string): Path or base64 data of the source scene image.
- `prompt` (string): Description of the motion or action in the video.
- `orientation` (string, optional): Orientation of the video, either "horizontal" or "vertical".

## Usage

To run the MCP server:

```bash
uv run server.py
```

### Claude Desktop Configuration

To integrate with Claude Desktop, add the following configuration to your `claude_desktop_config.json`:

```json
"mcpServers": {
  "ImageGeneratorWithFaceRef": {
    "command": "uv",
    "args": [
      "--directory",
      "/absolute/path/to/apps/mcp_gen_img_face_ref",
      "run",
      "server.py"
    ],
    "env": {
      "GEMINI_API_KEY": "your_api_key_here"
    }
  }
}
```

### Debug Mode

To run the server in debug mode using the Python MCP dev server (chạy ở mode debug):

```bash
mcp dev server.py
```

Or using the MCP CLI inspector:

```bash
npx @modelcontextprotocol/inspector uv run server.py
```
