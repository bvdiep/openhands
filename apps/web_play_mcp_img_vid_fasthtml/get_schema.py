import sys
import json
import asyncio
sys.path.append('/home/dd/work/diep/openhands/apps/mcp_gen_img_vid_with_refs')
from server import mcp

async def main():
    tools = await mcp.list_tools()
    schema = {}
    for t in tools:
        schema[t.name] = {
            "name": t.name,
            "description": t.description,
            "schema": t.inputSchema
        }
    print(json.dumps(schema))

asyncio.run(main())
