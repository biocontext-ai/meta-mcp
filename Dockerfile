FROM ubuntu:24.04

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH" \
    UV_CACHE_DIR=/opt/uv-cache \
    MCP_TRANSPORT=http \
    MCP_HOSTNAME=0.0.0.0 \
    MCP_PORT=8000

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -Ls https://astral.sh/uv/install.sh | sh
RUN uvx biocontext-meta --help

EXPOSE 8000

CMD ["uvx", "biocontext-meta"]
