FROM python:3.12-slim-bookworm@sha256:93ab4b7fa528b25124c97bcc755415e60eb671a86b4dbe0328df2fe2d1c1193d AS base

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

FROM base AS dependencies
COPY pyproject.toml README.md ./
COPY pdfquery/ pdfquery/
RUN uv pip install --system --no-cache -e .

FROM dependencies AS runtime
COPY --from=dependencies $APP_HOME $APP_HOME
COPY app.py .

RUN mkdir -p $APP_HOME/uploads && \
    groupadd -r appgroup && \
    useradd -r -g appgroup -d $APP_HOME -s /sbin/nologin appuser && \
    chown -R appuser:appgroup $APP_HOME

USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
