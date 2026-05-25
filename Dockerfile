# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm@sha256:93ab4b7fa528b25124c97bcc755415e60eb671a86b4dbe0328df2fe2d1c1193d

WORKDIR /app

# Security: patch OS packages (only updates with available fixes)
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Install uv (fast Rust-based Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY setup.py .
COPY pdfquery/ pdfquery/

# Install deps with persistent BuildKit cache — skips re-download on subsequent builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -e .

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
