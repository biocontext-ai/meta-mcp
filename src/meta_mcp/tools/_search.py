import json
from typing import Annotated

from meta_mcp.mcp import mcp


async def get_tool_info(
    server_name: Annotated[str, "The name of the server that provides the tool"],
    tool_name: Annotated[str, "The name of the tool to get information about"],
) -> str:
    """Returns the input schema for a given tool, to know how to call it."""
    if server_name not in mcp._tools or tool_name not in mcp._tools[server_name]:
        raise RuntimeError(f"Tool '{server_name}:{tool_name}' not found")
    tool_info = mcp._tools[server_name][tool_name]
    # Get the input_schema from the tool info
    input_schema = tool_info.get("input_schema", {})
    return json.dumps(input_schema)


async def list_servers() -> str:
    """Lists all available MCP servers and their descriptions, offering a wide range of tools for biomedical (analysis) tasks to choose from."""
    registry_df = mcp._registry_info
    if registry_df.empty:
        return json.dumps([])

    # Extract identifier and description columns
    result = []
    for _, row in registry_df.iterrows():
        server_info = {
            row.get("identifier"): row.get("description", ""),
        }
        result.append(server_info)

    return json.dumps(result)


async def list_server_tools(server_name: Annotated[str, "The name of the MCP server to list tools for"]) -> str:
    """Returns a list of all tools for a given MCP server."""
    # Check if server exists
    if server_name not in mcp._tools:
        raise RuntimeError(f"Server '{server_name}' not found in tools")
    if server_name not in mcp._servers:
        raise RuntimeError(f"Server '{server_name}' not found in servers")

    # Get tools from _tools dict (which contains both registry and connected tools)
    tool_info = []
    if server_name in mcp._tools:
        for tool_name, tool_data in mcp._tools[server_name].items():
            tool_info.append(
                {
                    tool_data.get("name", tool_name): tool_data.get("description", ""),
                }
            )

    return json.dumps(tool_info)
