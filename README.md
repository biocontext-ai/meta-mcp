# BioContext AI Meta MCP

[![BioContextAI - Registry](https://img.shields.io/badge/Registry-package?style=flat&label=BioContextAI&labelColor=%23fff&color=%233555a1&link=https%3A%2F%2Fbiocontext.ai%2Fregistry)](https://biocontext.ai/registry)
[![Tests][badge-tests]][tests]
[![Documentation][badge-docs]][documentation]

[badge-tests]: https://img.shields.io/github/actions/workflow/status/biocontext-ai/meta-mcp/test.yaml?branch=main
[badge-docs]: https://img.shields.io/readthedocs/meta-mcp

The BioContext AI Meta MCP enables access to all installable MCP servers in the BioContextAI registry with minimal context consumption.

## Getting started

Please refer to the [documentation][],
in particular, the [API documentation][].

You can also find the project on [BioContextAI](https://biocontext.ai), the community-hub for biomedical MCP servers: [meta-mcp on BioContextAI](https://biocontext.ai/registry/biocontext-ai/meta-mcp).

## Installation

You need to have Python 3.11 or newer installed on your system.
If you don't have Python installed, we recommend installing [uv][]. Internally we also make use of an LLM to generate structured tools calls, so you need to provide an API key for your chosen provider (OpenAI, Anthropic, or Google) as described below. The model can be changed by setting the `META_MCP_MODEL` environment variable or the `--model` flag, e.g., to `openai/gpt-5-nano` or `anthropic/claude-haiku-4-5-20251001`. We recommend using `openai/gpt-5-nano` or `openai/gpt-5-mini` for their guaranteed structured output support.

There are several alternative options to install meta-mcp:

### 1. Use `uvx` to run it immediately

From [PyPI]:

```bash
uvx biocontext-meta
```

Or from a Git repository:

```bash
uvx git+https://github.com/biocontext-ai/meta-mcp.git@main
```

### 2. Include it in one of various clients that supports the `mcp.json` standard

Pull the package from PyPI and start the server with the following configuration:

```json
{
  "mcpServers": {
    "meta-mcp": {
      "command": "uvx",
      "args": ["biocontext-meta"],
      "env": {
        "OPENAI_API_KEY": "YOUR OPENAI_API_KEY",
        "ANTHROPIC_API_KEY": "YOUR ANTHROPIC_API_KEY",
        "GEMINI_API_KEY": "YOUR GEMINI_API_KEY"
      }
    }
  }
}
```

From a Git repository:

```json
{
  "mcpServers": {
    "meta-mcp": {
      "command": "uvx",
      "args": ["git+https://github.com/biocontext-ai/meta-mcp.git@main"],
      "env": {
        "OPENAI_API_KEY": "YOUR OPENAI_API_KEY",
        "ANTHROPIC_API_KEY": "YOUR ANTHROPIC_API_KEY",
        "GEMINI_API_KEY": "YOUR GEMINI_API_KEY"
      }
    }
  }
}
```

For purely local development (e.g., in Cursor or VS Code), use the following configuration (you can also provide API keys in an `.env` file):

```json
{
  "mcpServers": {
    "meta-mcp": {
      "command": "uvx",
      "args": [
        "--refresh",
        "--from",
        "path/to/repository",
        "biocontext-meta"
      ],
      "env": {
        "OPENAI_API_KEY": "YOUR OPENAI_API_KEY",
        "ANTHROPIC_API_KEY": "YOUR ANTHROPIC_API_KEY",
        "GEMINI_API_KEY": "YOUR GEMINI_API_KEY"
      }
    }
  }
}
```

If you want to reuse an existing environment for local development, use the following configuration (you can also provide API keys in an `.env` file):

```json
{
  "mcpServers": {
    "meta-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "path/to/repository", "biocontext-meta"],
      "env": {
        "OPENAI_API_KEY": "YOUR OPENAI_API_KEY",
        "ANTHROPIC_API_KEY": "YOUR ANTHROPIC_API_KEY",
        "GEMINI_API_KEY": "YOUR GEMINI_API_KEY"
      }
    }
  }
}
```

### 3. Install it through `pip`

```bash
pip install --user biocontext-meta
```

### 4. Install the latest development version

```bash
pip install git+https://github.com/biocontext-ai/meta-mcp.git@main
```

## Docker (streamable HTTP)

The Docker image runs the MCP server in streamable HTTP mode by default (`MCP_TRANSPORT=http`) and listens on port 8000.

Build the image:

```bash
docker build -t biocontext-meta .
```

Run the server:

```bash
docker run --rm -p 8000:8000 \
  -e OPENAI_API_KEY=YOUR_OPENAI_API_KEY \
  -e ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY \
  -e GEMINI_API_KEY=YOUR_GEMINI_API_KEY \
  biocontext-meta
```

Override transport/host/port if needed:

```bash
docker run --rm -p 9000:9000 \
  -e MCP_TRANSPORT=http \
  -e MCP_HOSTNAME=0.0.0.0 \
  -e MCP_PORT=9000 \
  biocontext-meta
```

To access the MCP server from a client, you can use the following URL: `http://localhost:8000/mcp` or the following `mcp.json` configuration:

```json
{
  "mcpServers": {
    "meta-mcp": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## Configuration

The CLI supports flags and equivalent environment variables for all options:

- `--transport` / `MCP_TRANSPORT` (default: `stdio`)
- `--host` / `MCP_HOSTNAME` (default: `0.0.0.0`)
- `--port` / `MCP_PORT` (default: `8000`)
- `--connect-on-startup` / `MCP_CONNECT_ON_STARTUP` (not recommended)
- `--registry-json` / `MCP_REGISTRY_JSON` (default: `https://biocontext.ai/registry.json`)
- `--registry-mcp-json` / `MCP_REGISTRY_MCP_JSON` (default: `https://biocontext.ai/mcp.json`)
- `--registry-mcp-tools-json` / `MCP_REGISTRY_MCP_TOOLS_JSON` (default: `https://biocontext.ai/mcp_tools.json`)
- `--model` / `META_MCP_MODEL` (default: `openai/gpt-5-nano`)
- `--search-mode` / `MCP_SEARCH_MODE` (`string_match`, `llm`, `semantic`; default: `llm`)
- `--reasoning` / `META_MCP_REASONING` (default: `false`)
- `--max-servers` / `MCP_MAX_SERVERS` (default: `10`)
- `--max-tools` / `MCP_MAX_TOOLS` (default: `10`)
- `--output-args` / `META_MCP_OUTPUT_ARGS` (default: `false`)
- `--version` (print package version)

Semantic search (`--search-mode semantic`) uses `sentence-transformers` by default with model `all-MiniLM-L6-v2`, which downloads on first use. For an HTTP embedding backend, set `META_MCP_EMBEDDING_HTTP_URL` (default: `http://127.0.0.1:8501/embed`).

## How it works

The BioContext AI Meta MCP provides dynamic access to MCP servers from the BioContextAI registry with minimal context consumption. It works through several key mechanisms:

- **Dynamic server connections**: Automatically connects to and manages MCP servers on-demand, loading configurations and tool metadata from remote JSON registries
- **LLM-powered search**: Uses AI to intelligently search and filter available servers and tools across multiple modes (string matching, semantic search, and LLM-based reasoning)
- **Structured output generation**: Leverages LiteLLM integration to generate properly structured tool calls with JSON schema validation and Pydantic model generation
- **Tool exploration**: Provides dynamic discovery and exploration of available tools with configurable result limits and comprehensive metadata access

## Known Issues

- When using the `--connect-on-startup` flag, the server might have trouble starting, depending on the client

## Contact

If you found a bug, please use the [issue tracker][].

## Citation

If this MCP server is useful to your research, please cite the BioContextAI publication:

```bibtex
@article{BioContext_AI_Kuehl_Schaub_2025,
  title={BioContextAI is a community hub for agentic biomedical systems},
  url={http://dx.doi.org/10.1038/s41587-025-02900-9},
  urldate = {2025-11-06},
  doi={10.1038/s41587-025-02900-9},
  year = {2025},
  month = nov,
  journal={Nature Biotechnology},
  publisher={Springer Science and Business Media LLC},
  author={Kuehl, Malte and Schaub, Darius P. and Carli, Francesco and Heumos, Lukas and Hellmig, Malte and Fernández-Zapata, Camila and Kaiser, Nico and Schaul, Jonathan and Kulaga, Anton and Usanov, Nikolay and Koutrouli, Mikaela and Ergen, Can and Palla, Giovanni and Krebs, Christian F. and Panzer, Ulf and Bonn, Stefan and Lobentanzer, Sebastian and Saez-Rodriguez, Julio and Puelles, Victor G.},
  year={2025},
  month=nov,
  language={en},
}
```

[uv]: https://github.com/astral-sh/uv
[issue tracker]: https://github.com/biocontext-ai/meta-mcp/issues
[tests]: https://github.com/biocontext-ai/meta-mcp/actions/workflows/test.yaml
[documentation]: https://meta-mcp.readthedocs.io
[changelog]: https://meta-mcp.readthedocs.io/en/latest/changelog.html
[api documentation]: https://meta-mcp.readthedocs.io/en/latest/api.html
[pypi]: https://pypi.org/project/biocontext-meta
