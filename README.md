# CCEP-RAG

> Content extraction + RAG query. Upload PDFs → ask questions. Built for Asseco recruitment.

## Quick Start

```bash
git clone <repo-url>
cd ccep-rag
pip install -e .
cp .env.example .env
# Edit .env: set GROQ_API_KEY, optionally COHERE_API_KEY
ccep ingest some-document.pdf
ccep query "What does this document say?"
```

## Web UI

```bash
streamlit run app.py
# Open http://localhost:8501
```

## Docker

```bash
docker compose up
# Open http://localhost:8501
```

## Architecture

```
PDF → extract (pdfplumber) → chunk → embed (Cohere/local) → Chroma DB → retrieve → Groq LLM → answer
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| PDF extraction | pdfplumber |
| Embeddings | Cohere Embed v3 or sentence-transformers (fallback) |
| Vector DB | Chroma |
| LLM | Groq (Llama 3.3 70B) |
| Web UI | Streamlit |
| CI/CD | Jenkins + GitHub Actions |
| Container | Docker + docker-compose |
| Orchestration | k3s + Helm (optional) |

## DevOps

- `Jenkinsfile` — build, test, push to GHCR
- `Dockerfile` + `docker-compose.yml` — one-command deploy
- Helm chart at `helm/` — K8s deployment with rollback

## Live Demo

[https://rag.zachara.com](https://rag.zachara.com)
