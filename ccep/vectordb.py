import psycopg2
import psycopg2.extras
from ccep.config import DATABASE_URL
from ccep.models import Chunk
from ccep.embedder import Embedder


class VectorDB:
    def __init__(self):
        self._embedder = Embedder()
        self._conn = psycopg2.connect(DATABASE_URL)
        self._init_db()

    def _init_db(self):
        with self._conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    doc_id TEXT NOT NULL,
                    heading TEXT DEFAULT '',
                    text TEXT NOT NULL,
                    embedding vector(1024),
                    idx INT DEFAULT 0
                )
            """)
            cur.execute("CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON chunks(doc_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON chunks USING hnsw (embedding vector_cosine_ops)")
        self._conn.commit()

    def ingest(self, chunks: list[Chunk]):
        if not chunks:
            return
        embeddings = self._embedder.embed_documents(chunks)
        with self._conn.cursor() as cur:
            for c, emb in zip(chunks, embeddings):
                cur.execute(
                    "INSERT INTO chunks (id, doc_id, heading, text, embedding, idx) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (f"{c.doc_id}_{c.index}", c.doc_id, c.heading, c.text, emb, c.index),
                )
        self._conn.commit()

    def query(self, question: str, top_k: int = 3) -> list[dict]:
        query_embedding = self._embedder.embed_query(question)
        with self._conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                "SELECT text, heading, doc_id, "
                "1 - (embedding <=> %s::vector) AS score "
                "FROM chunks "
                "ORDER BY embedding <=> %s::vector "
                "LIMIT %s",
                (query_embedding, query_embedding, top_k),
            )
            rows = cur.fetchall()
            return [
                {
                    "text": r["text"],
                    "heading": r["heading"],
                    "doc_id": r["doc_id"],
                    "score": float(r["score"]),
                }
                for r in rows
            ]

    def clear(self):
        with self._conn.cursor() as cur:
            cur.execute("DELETE FROM chunks")
        self._conn.commit()

    def list_docs(self) -> list[str]:
        with self._conn.cursor() as cur:
            cur.execute("SELECT DISTINCT doc_id FROM chunks")
            return [r[0] for r in cur.fetchall()]
