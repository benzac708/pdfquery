# PDFQuery — RAG Question-Answering System

```json
{"live": "https://rag.zachara.dev", "repo": "benzac708/pdfquery"}
```

Upload a PDF, ask questions in natural language, get answers with source snippets.

## Architecture

```
PDF upload → extract text → chunk → embed (Cohere) → pgvector → semantic search → LLM answer (Groq)
```

Split into three tiers:
- **CLI** (Python) — ingest PDFs and query via terminal
- **Web UI** (Streamlit) — drag-and-drop upload, chat interface
- **CI/CD** (Jenkins) — automated build, scan, sign, deploy pipeline

## Tech Stack

| Layer | Tool | Usage |
|-------|------|-------|
| Language | Python 3.12 | App logic, CLI, Streamlit backend |
| Embeddings | Cohere `embed-multilingual-v3.0` | Converts text chunks to 1024-dim vectors |
| LLM | Groq `llama-3.3-70b-versatile` | Generates answer from retrieved context |
| Database | PostgreSQL + pgvector (HNSW index) | Stores and searches document vectors |
| Container | Docker + Docker Compose | Multi-stage build, pinned base image digests |
| CI/CD | Jenkins (JCasC) | Auto-triggered on push — lint → scan → test → build → Trivy → cosign → deploy → smoke test |
| Registry | GHCR | Signed OCI images with SBOM |
| Security | Cloudflare Tunnel | Public ingress without open ports |

## Pipeline (Jenkins)

Every push to `main`:
1. **Ruff** — lint check + auto-fix
2. **Gitleaks** — secrets scan
3. **pytest** — import verification
4. **Docker build** — with SBOM generation
5. **Trivy** — CRITICAL vulnerability scan (fail on any)
6. **cosign sign** — image signing with key pair
7. **cosign verify** — signature check before deploy
8. **Deploy** — docker-compose pull + up on VPS
9. **Smoke test** — HTTP health check (10 retries)

## Quick Start

```bash
cp .env.example .env
# set GROQ_API_KEY and COHERE_API_KEY
uv venv .venv && uv pip install -e .
docker compose up -d db
source .venv/bin/activate && streamlit run app.py
```

### CLI

```bash
pdfquery ingest path/to/file.pdf
pdfquery query "What does this say about X?"
```

### Docker

```bash
docker compose up -d --build
```

## Environment

| Variable | Required | Default |
|----------|----------|---------|
| `GROQ_API_KEY` | Yes | — |
| `COHERE_API_KEY` | Yes | — |
| `DATABASE_URL` | No | `postgresql+psycopg://...` |
| `CHUNK_SIZE` | No | 500 |
| `CHUNK_OVERLAP` | No | 50 |
| `TOP_K` | No | 3 |
