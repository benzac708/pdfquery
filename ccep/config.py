import os
from pathlib import Path

CCEP_DIR = Path(__file__).parent.parent

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY", "")

CHROMA_DIR = os.environ.get("CHROMA_DIR", str(CCEP_DIR / "chroma_db"))
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", str(CCEP_DIR / "uploads"))

CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", "50"))
TOP_K = int(os.environ.get("TOP_K", "10"))
