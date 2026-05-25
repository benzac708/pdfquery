# pdfquery — Project Context for AI Assistants

## Structure
- `pdfquery/` — Python package: extractor, chunker, embedder, vectordb, rag, cli
- `app.py` — Streamlit web GUI
- `setup.py` — package install (`pip install -e .`)
- `Dockerfile` + `docker-compose.yml` — containerized deployment

## Stack
- Python 3.12, Streamlit, pdfplumber, pgvector (PostgreSQL)
- Embeddings: Cohere API v3
- LLM: Groq API (Llama 3.3 70B)
- Docker Compose (app + pgvector), GH Actions CI/CD

## Commands
- `pdfquery ingest <file.pdf>` — extract, chunk, embed, store
- `pdfquery query <question>` — retrieve + answer via Groq
- `streamlit run app.py` — web UI on :8501
- `docker compose up` — full stack

## Env
- Copy `.env.example` → `.env`
- `GROQ_API_KEY` — from console.groq.com
- `COHERE_API_KEY` — from dashboard.cohere.com (optional, falls back to local)
- Cohere is the only embedding provider — COHERE_API_KEY required

## Rules
- No hardcoded paths — use `pdfquery/config.py` env vars
- No secrets in repo — use `.env` or K8s Secrets
- Python type hints required on all functions
- Keep Streamlit `app.py` under 100 lines
