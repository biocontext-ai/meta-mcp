import enum
import logging
import os
import sys

import click


class EnvironmentType(enum.Enum):
    """Enum to define environment type."""

    PRODUCTION = enum.auto()
    DEVELOPMENT = enum.auto()


@click.command(name="run")
@click.option(
    "-t",
    "--transport",
    "transport",
    type=str,
    help="MCP transport option. Defaults to 'stdio'.",
    default="stdio",
    envvar="MCP_TRANSPORT",
)
@click.option(
    "-p",
    "--port",
    "port",
    type=int,
    help="Port of MCP server. Defaults to '8000'",
    default=8000,
    envvar="MCP_PORT",
    required=False,
)
@click.option(
    "-h",
    "--host",
    "hostname",
    type=str,
    help="Hostname of MCP server. Defaults to '0.0.0.0'",
    default="0.0.0.0",
    envvar="MCP_HOSTNAME",
    required=False,
)
@click.option("-v", "--version", "version", is_flag=True, help="Get version of package.")
@click.option(
    "-e",
    "--env",
    "environment",
    type=click.Choice(EnvironmentType, case_sensitive=False),
    default=EnvironmentType.DEVELOPMENT,
    envvar="MCP_ENVIRONMENT",
    help="MCP server environment. Defaults to 'development'.",
)
@click.option(
    "--connect-on-startup",
    "connect_on_startup",
    is_flag=True,
    default=False,
    help="Connect to MCP servers on startup. Sets MCP_CONNECT_ON_STARTUP environment variable.",
)
@click.option(
    "--registry-json",
    "registry_json",
    type=str,
    help="URL or path to registry.json file. Defaults to 'https://biocontext.ai/registry.json'.",
    default=None,
    envvar="MCP_REGISTRY_JSON",
)
@click.option(
    "--registry-mcp-json",
    "registry_mcp_json",
    type=str,
    help="URL or path to mcp.json file. Defaults to 'https://biocontext.ai/mcp.json'.",
    default=None,
    envvar="MCP_REGISTRY_MCP_JSON",
)
@click.option(
    "--registry-mcp-tools-json",
    "registry_mcp_tools_json",
    type=str,
    help="URL or path to mcp_tools.json file. Defaults to 'https://biocontext.ai/mcp_tools.json'.",
    default=None,
    envvar="MCP_REGISTRY_MCP_TOOLS_JSON",
)
@click.option(
    "--model",
    "model",
    type=str,
    help="Model name to use for structured output generation. Defaults to 'gpt-4.1-mini'.",
    default=None,
    envvar="META_MCP_MODEL",
)
def run_app(
    transport: str = "stdio",
    port: int = 8000,
    hostname: str = "0.0.0.0",
    environment: EnvironmentType = EnvironmentType.DEVELOPMENT,
    version: bool = False,
    connect_on_startup: bool = False,
    registry_json: str | None = None,
    registry_mcp_json: str | None = None,
    registry_mcp_tools_json: str | None = None,
    model: str | None = None,
):
    """Run the MCP server "meta-mcp".

    The BioContext AI meta mcp enables access to all installable MCP servers in the BioContextAI registry with minimal context consumption.
    If the environment variable MCP_ENVIRONMENT is set to "PRODUCTION", it will run the Starlette app with streamable HTTP for the MCP server. Otherwise, it will run the MCP server via stdio.
    The port is set via "-p/--port" or the MCP_PORT environment variable, defaulting to "8000" if not set.
    The hostname is set via "-h/--host" or the MCP_HOSTNAME environment variable, defaulting to "0.0.0.0" if not set.
    To specify to transform method of the MCP server, set "-e/--env" or the MCP_TRANSPORT environment variable, which defaults to "stdio".
    """
    if version is True:
        from meta_mcp import __version__

        click.echo(__version__)
        sys.exit(0)

    # Set environment variables based on CLI flags BEFORE importing modules that use mcp
    os.environ["MCP_CONNECT_ON_STARTUP"] = "true" if connect_on_startup else "false"

    if registry_json is not None:
        os.environ["MCP_REGISTRY_JSON"] = registry_json
    if registry_mcp_json is not None:
        os.environ["MCP_REGISTRY_MCP_JSON"] = registry_mcp_json
    if registry_mcp_tools_json is not None:
        os.environ["MCP_REGISTRY_MCP_TOOLS_JSON"] = registry_mcp_tools_json
    if model is not None:
        os.environ["META_MCP_MODEL"] = model

    logger = logging.getLogger(__name__)

    from meta_mcp.mcp import mcp

    # Import tools after setting environment variables so conditional imports work
    # This ensures __all__ is populated correctly based on environment variables
    from . import tools

    # Register all tools from __all__ dynamically
    for name in tools.__all__:
        tool_func = getattr(tools, name)
        mcp.tool(tool_func)

    if environment == EnvironmentType.DEVELOPMENT:
        logger.info("Starting MCP server (DEVELOPMENT mode)")
        if transport == "http":
            mcp.run(transport=transport, port=port, host=hostname)
        else:
            mcp.run(transport=transport)
    else:
        raise NotImplementedError()
        # logger.info("Starting Starlette app with Uvicorn in PRODUCTION mode.")
        # uvicorn.run(app, host=hostname, port=port)


if __name__ == "__main__":
    run_app()
