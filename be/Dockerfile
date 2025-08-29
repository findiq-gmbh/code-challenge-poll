FROM python:3.12-slim

WORKDIR /app
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache
COPY . .
RUN mkdir -p /app/data
EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
