import json
from typing import Annotated

from json_schema_to_pydantic import create_model
from pydantic import create_model as pydantic_create_model

from meta_mcp.mcp import mcp
from meta_mcp.utils import (
    SchemaReasoningOutput,
    fix_schema,
    get_structured_response_litellm,
    structured_response_to_output_model,
)


async def call_tool(
    server_name: Annotated[str, "The name of the server that provides the tool"],
    tool_name: Annotated[str, "The name of the tool to call"],
    arguments: Annotated[str, "The arguments to pass to the tool"],
) -> str:
    """Call a tool with the given arguments. Returns the output of the called tool."""
    # Check if server is connected, if not try to connect it from registry
    try:
        client = mcp.get_client(server_name)
    except RuntimeError:
        # Server not connected, try to connect it from registry
        if server_name in mcp._servers:
            await mcp.connect_to_server(server_name)
            client = mcp.get_client(server_name)
        else:
            raise RuntimeError(f"Server '{server_name}' not found in registry") from None

    if server_name not in mcp._tools or tool_name not in mcp._tools[server_name]:
        raise RuntimeError(f"Tool '{server_name}:{tool_name}' not found")
    tool_info = mcp._tools[server_name][tool_name]
    # Get the input_schema from the tool info
    input_schema = tool_info.get("input_schema", {})

    # Fix schemas with prefixItems but no items (json_schema_to_pydantic requires items)
    # Fix the schema before creating the model
    if input_schema:
        input_schema = fix_schema(input_schema)

    # Convert JSON schema to Pydantic model
    pydantic_model = create_model(input_schema)
    reasoning = True
    if reasoning:
        pydantic_model = pydantic_create_model(
            pydantic_model.__name__, __base__=(pydantic_model, SchemaReasoningOutput)
        )
    try:
        response = get_structured_response_litellm(
            input=arguments,
            system_prompt="You will be given an input string, containing argument values, carefully convert it to the given output schema. The input might have errors or ambiguities, try to fix these using the descriptions in the output schema.",
            output_model=pydantic_model,
        )
        output_parsed = structured_response_to_output_model(response, pydantic_model)
        output_parsed_dict = output_parsed.model_dump()
        output_parsed_dict.pop("schema_reasoning", None)
        call_result = await client.call_tool(tool_name, arguments=output_parsed_dict or {})

        result = {
            "content": [block.model_dump() for block in call_result.content],
        }
        return json.dumps(result)
    except (RuntimeError, ValueError, KeyError, TypeError) as e:
        return f"Failed to call tool: {e}"
