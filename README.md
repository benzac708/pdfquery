# PDFQuery

Live: https://rag.zachara.dev
Pipeline: push → Jenkins → Ruff → Gitleaks → build → Trivy → cosign → deploy → smoke

## Commands

```bash
# setup
cp .env.example .env    # set GROQ_API_KEY, COHERE_API_KEY
uv venv .venv && source .venv/bin/activate
uv pip install -e .

# run
docker compose up -d    # db + app
streamlit run app.py    # or open localhost:8501

# cli
pdfquery ingest ~/file.pdf
pdfquery query "pytanie"

# db
docker compose up -d db           # db only
docker compose down -v            # reset everything
docker exec -it pdfquery-db-1 psql -U ccep -d ccep
# then: \dt, SELECT * FROM chunks LIMIT 5;

# build & push
docker build -t ghcr.io/benzac708/pdfquery:latest .
docker push ghcr.io/benzac708/pdfquery:latest

# deploy on vps
docker pull ghcr.io/benzac708/pdfquery:latest
docker compose -p pdfquery -f /app/docker-compose.yml down
docker compose -p pdfquery -f /app/docker-compose.yml up -d
curl http://127.0.0.1:8501/_stcore/health

# security
docker run --rm aquasec/trivy:latest image pdfquery:latest
docker run --rm -v "$PWD:/repo" ghcr.io/gitleaks/gitleaks:latest detect --source /repo

# jenkins (local scripts)
bash scripts/jenkins-status.sh
bash scripts/jenkins-tail.sh [build]
bash scripts/jenkins-trigger.sh

# cosign
cosign generate-key-pair
COSIGN_PASSWORD="" cosign sign --key cosign.key ghcr.io/benzac708/pdfquery:abc123
cosign verify --key cosign.pub ghcr.io/benzac708/pdfquery:abc123

# logs
docker compose logs -f app
docker compose logs -f db
```

### Struktura

```
pdfquery/             # Python package
├── cli.py, extractor.py, chunker.py
├── embedder.py, vectordb.py, rag.py
└── config.py, models.py
app.py, Dockerfile, docker-compose.yml, Jenkinsfile
```
