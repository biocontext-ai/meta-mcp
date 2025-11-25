# meta-mcp

[![BioContextAI - Registry](https://img.shields.io/badge/Registry-package?style=flat&label=BioContextAI&labelColor=%23fff&color=%233555a1&link=https%3A%2F%2Fbiocontext.ai%2Fregistry)](https://biocontext.ai/registry)
[![Tests][badge-tests]][tests]
[![Documentation][badge-docs]][documentation]

[badge-tests]: https://img.shields.io/github/actions/workflow/status/biocontext-ai/meta-mcp/test.yaml?branch=main
[badge-docs]: https://img.shields.io/readthedocs/meta-mcp

The BioContext AI meta mcp enables access to all installable MCP servers in the BioContextAI registry with minimal context consumption.

## Getting started

Please refer to the [documentation][],
in particular, the [API documentation][].

You can also find the project on [BioContextAI](https://biocontext.ai), the community-hub for biomedical MCP servers: [meta-mcp on BioContextAI](https://biocontext.ai/registry/biocontext-ai/meta-mcp).

## Installation

You need to have Python 3.11 or newer installed on your system.
If you don't have Python installed, we recommend installing [uv][]. Internally we also make use of GPT-4.1-mini to generate structured tools calls, so you need to provide an OpenAI API key as described below. The model can be changed by setting the `META_MCP_MODEL` environment variable or the `--model` flag, e.g., to `openai/gpt-5-nano`.

There are several alternative options to install meta-mcp:

### 1. Use `uvx` to run it immediately
After publication to PyPI:
```bash
uvx meta-mcp
```

Or from a Git repository:

```bash
uvx git+https://github.com/biocontext-ai/meta-mcp.git@main
```

### 2. Include it in one of various clients that supports the `mcp.json` standard

If your MCP server is published to PyPI, use the following configuration:

```json
{
  "mcpServers": {
    "meta-mcp": {
      "command": "uvx",
      "args": ["meta-mcp"],
      "env": {
        "OPENAI_API_KEY": "YOUR OPENAI_API_KEY",
      }
    }
  }
}
```
In case the MCP server is not yet published to PyPI, use this configuration:

```json
{
  "mcpServers": {
    "meta-mcp": {
      "command": "uvx",
      "args": ["git+https://github.com/biocontext-ai/meta-mcp.git@main"],
      "env": {
        "OPENAI_API_KEY": "YOUR OPENAI_API_KEY",
      }
    }
  }
}
```

For purely local development (e.g., in Cursor or VS Code), use the following configuration (you can also provide the OPENAI_API_KEY in an `.env` file):

```json
{
  "mcpServers": {
    "meta-mcp": {
      "command": "uvx",
      "args": [
        "--refresh",
        "--from",
        "path/to/repository",
        "meta-mcp"
      ],
      "env": {
        "OPENAI_API_KEY": "YOUR OPENAI_API_KEY",
      }
    }
  }
}
```

If you want to reuse an existing environment for local development, use the following configuration (you can also provide the OPENAI_API_KEY in an `.env` file):

```json
{
  "mcpServers": {
    "meta-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "path/to/repository", "meta-mcp"],
      "env": {
        "OPENAI_API_KEY": "YOUR OPENAI_API_KEY",
      }
    }
  }
}
```

### 3. Install it through `pip`:

```bash
pip install --user meta-mcp
```

### 4. Install the latest development version:

```bash
pip install git+https://github.com/biocontext-ai/meta-mcp.git@main
```

## Known Issues
- When using the `--connect-on-startup` flag, the server might have trouble starting, depending on the client

## Contact

If you found a bug, please use the [issue tracker][].

## Citation

> t.b.a

[uv]: https://github.com/astral-sh/uv
[issue tracker]: https://github.com/biocontext-ai/meta-mcp/issues
[tests]: https://github.com/biocontext-ai/meta-mcp/actions/workflows/test.yaml
[documentation]: https://meta-mcp.readthedocs.io
[changelog]: https://meta-mcp.readthedocs.io/en/latest/changelog.html
[api documentation]: https://meta-mcp.readthedocs.io/en/latest/api.html
[pypi]: https://pypi.org/project/meta-mcp
