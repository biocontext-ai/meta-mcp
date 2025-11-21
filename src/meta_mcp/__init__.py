from importlib.metadata import version

from meta_mcp.main import run_app
from meta_mcp.mcp import mcp

__version__ = version("meta-mcp")

__all__ = ["mcp", "run_app", "__version__"]


if __name__ == "__main__":
    run_app()
