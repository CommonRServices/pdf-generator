FROM python:3.13.11-slim-bookworm AS playwright-base

RUN pip install --no-cache-dir playwright==1.57.0 && playwright install --with-deps

RUN apt-get update && apt-get install --no-install-recommends -y \
    ghostscript=10.* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


FROM playwright-base AS app

COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY app .

ENTRYPOINT ["uv", "run", "fastapi", "run", "--workers", "4"]