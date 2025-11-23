import pytest
from fastmcp import Client

import meta_mcp
from meta_mcp import tools
from meta_mcp.mcp import mcp


def test_package_has_version():
    """Testing package version exist."""
    assert meta_mcp.__version__ is not None


@pytest.mark.asyncio
async def test_mcp_server():
    """Testing MCP server."""
    # Register all tools from tools module
    for name in tools.__all__:
        tool_func = getattr(tools, name)
        mcp.tool(tool_func)

    async with Client(mcp) as client:
        server = "biocontext-ai/anndata-mcp"
        result = await client.call_tool("list_server_tools", {"server_name": server})
        print(f"Tools for server '{server}':", result.content)

        # Example: Get tool info using tuple-based keys (separate server_name and tool_name)
        result = await client.call_tool("get_tool_info", {"server_name": server, "tool_name": "get_summary"})
        print(f"Tool info for '{server}:get_summary':", result.content)
