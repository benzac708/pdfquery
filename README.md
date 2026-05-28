# PDFQuery

Live: https://rag.zachara.dev
Pipeline: Jenkins (push → Ruff → Gitleaks → test → build → Trivy → cosign → deploy → smoke)

Local RAG: upload PDF → extract text → chunk → embed (Cohere) → pgvector → LLM answer (Groq).

## Commands

### Local setup

```bash
git clone https://github.com/benzac708/pdfquery && cd pdfquery
cp .env.example .env
# set GROQ_API_KEY and COHERE_API_KEY in .env
uv venv .venv && source .venv/bin/activate
uv pip install -e .
```

### Database

```bash
# start PostgreSQL with pgvector
docker compose up -d db
docker compose down -v    # delete everything + rebuild from scratch

# connect and query
docker exec -it pdfquery-db-1 psql -U ccep -d ccep
# then: \dt, SELECT * FROM chunks LIMIT 5;
```

### CLI

```bash
pdfquery ingest ~/some.pdf
pdfquery query "co mówi o x?"
```

### Streamlit UI

```bash
streamlit run app.py
# opens at localhost:8501
```

### Docker

```bash
docker compose up -d --build      # local full stack (db + app)
docker compose logs -f app        # follow app logs
docker compose ps                 # status
```

### VPS deploy (manual, instead of Jenkins)

```bash
# on VPS:
docker pull ghcr.io/benzac708/pdfquery:latest
docker compose -p pdfquery -f /app/docker-compose.yml down
docker compose -p pdfquery -f /app/docker-compose.yml up -d
# check: curl http://127.0.0.1:8501/_stcore/health
```

### Jenkins

```bash
# local helpers in scripts/
bash scripts/jenkins-status.sh          # last build status
bash scripts/jenkins-tail.sh [build]    # console log
bash scripts/jenkins-trigger.sh         # queue new build
```

Jenkins config in `jenkins/jenkins.yaml` (JCasC). Pipeline in `Jenkinsfile`.

### Image sign (cosign)

```bash
# generate key pair
cosign generate-key-pair
# sign
COSIGN_PASSWORD="" cosign sign --key cosign.key ghcr.io/benzac708/pdfquery:abc123
# verify
cosign verify --key cosign.pub ghcr.io/benzac708/pdfquery:abc123
```

### Security scan

```bash
# local trivy
docker run --rm aquasec/trivy:latest image pdfquery:latest
# gitleaks
docker run --rm -v "$PWD:/repo" ghcr.io/gitleaks/gitleaks:latest detect --source /repo
```

### Troubleshooting

```bash
# app crash on start — check logs
docker compose logs app

# database not connecting
docker compose logs db
docker exec -it pdfquery-db-1 pg_isready -U ccep

# chat stuck "upload document first" — session state issue
# refresh browser, re-upload PDF

# "Readme file does not exist" — Dockerfile missing pyproject dependency
# COPY pyproject.toml README.md ./
```

## Project structure

```
pdfquery/             # Python package
├── cli.py            # pdfquery ingest/query
├── extractor.py      # pdfplumber, text extraction
├── chunker.py        # split text into chunks
├── embedder.py       # Cohere API → vectors
├── vectordb.py       # PostgreSQL + pgvector SQL
├── rag.py            # Groq API → answer from context
├── config.py         # env vars
└── models.py         # data classes
app.py                # Streamlit UI
Dockerfile            # multi-stage build
docker-compose.yml    # app + db
Jenkinsfile           # CI/CD pipeline
```
