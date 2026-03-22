import sys
import asyncio
sys.path.append('/home/dd/work/diep/openhands/apps/mcp_gen_img_vid_with_refs')
from server import mcp

async def main():
    tools = await mcp.list_tools()
    for t in tools:
        print(t.name)
        print(t.inputSchema)

asyncio.run(main())
