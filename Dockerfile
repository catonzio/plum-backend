FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /uvx /bin/

COPY . /plum-backend

WORKDIR /plum-backend

RUN apt-get update && apt-get install -y \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN uv sync

# CMD ["uv", "run", "gradio", "src/plum-backend/main.py"]
