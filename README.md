# PDFQuery

GitHub repo: `benzac708/pdfquery`

PDF question-answering app with a small CLI and Streamlit UI.

## What it does

- upload a PDF
- extract text
- chunk it
- embed and store it in PostgreSQL + pgvector
- ask questions with source snippets

## Stack

- Python 3.12
- Streamlit
- PostgreSQL + pgvector
- Cohere `embed-multilingual-v3.0` for embeddings
- Groq `llama-3.3-70b-versatile` for answer generation
- Docker + Docker Compose
- Jenkins CI/CD
- GHCR image registry
- Cloudflare Tunnel for public access

## Local run

```bash
cp .env.example .env
# set GROQ_API_KEY and COHERE_API_KEY
pip install -e .
docker compose up -d db
streamlit run app.py
```

## CLI

```bash
pdfquery ingest path/to/file.pdf
pdfquery query "What does this say about X?"
```

## Docker

```bash
docker compose up -d --build
```

## Environment

Required:

- `GROQ_API_KEY`
- `COHERE_API_KEY`

Optional:

- `DATABASE_URL`
- `CHUNK_SIZE`
- `CHUNK_OVERLAP`
- `TOP_K`

## CI/CD

- lint with Ruff
- scan secrets with Gitleaks
- test in a Python venv with `uv`
- build and push a tagged image to GHCR
- scan the image with Trivy
- sign the image with cosign
- deploy by pulling the exact image tag
- run a post-deploy smoke test
