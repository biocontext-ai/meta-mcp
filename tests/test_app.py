import json

import pytest
from fastmcp import Client

import meta_mcp


def test_package_has_version():
    """Testing package version exist."""
    assert meta_mcp.__version__ is not None


@pytest.mark.asyncio
async def test_mcp_server():
    """Testing MCP server."""
    async with Client(meta_mcp.mcp) as client:
        server = "biocontext-ai/anndata-mcp"
        # result = await client.call_tool("list_server_tools", {"server_name": server})
        # print(f"Tools for server '{server}':", result.content)

        # # Example: Get tool info using tuple-based keys (separate server_name and tool_name)
        # result = await client.call_tool("get_tool_info", {"server_name": server, "tool_name": "get_summary"})
        # print(f"Tool info for '{server}:get_summary':", result.content)
        # # print(f"Tool info for '{server}:get_summary':", result.content)

        # # call a tool
        # result = await client.call_tool(
        #     "call_tool",
        #     {
        #         "server_name": server,
        #         "tool_name": "get_summary",
        #         "arguments": "/home/dschaub/projects/biocontext_ai/anndata-mcp/data/test.h5ad",
        #     },
        # )
        # print(f"Tool result for '{server}:get_summary':", result.content)

        result = await client.call_tool(
            "call_tool",
            {
                "server_name": server,
                "tool_name": "get_descriptive_stats",
                "arguments": json.dumps(
                    {
                        "path": "/home/dschaub/projects/biocontext_ai/scverse-2025-workshop/data/pbmc3k_processed.h5ad",
                        "attribute": "obs",
                    }
                ),
            },
        )
        print(f"Tool result for '{server}:get_descriptive_stats':", result.content)

        result = await client.call_tool(
            "call_tool",
            {
                "server_name": server,
                "tool_name": "view_raw_data",
                "arguments": json.dumps(
                    {
                        "path": "/home/dschaub/projects/biocontext_ai/scverse-2025-workshop/data/pbmc3k_processed.h5ad",
                        "attribute": "var",
                        "row_start_index": 0,
                        "row_stop_index": 10,
                    }
                ),
            },
        )
        print(f"Tool result for '{server}:view_raw_data':", result.content)
