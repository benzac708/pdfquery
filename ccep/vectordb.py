from ccep.config import CHROMA_DIR
from ccep.models import Chunk
from ccep.embedder import Embedder
import chromadb


class VectorDB:
    def __init__(self):
        self._client = chromadb.PersistentClient(path=CHROMA_DIR)
        self._embedder = Embedder()

    def _collection(self):
        return self._client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
        )

    def ingest(self, chunks: list[Chunk]):
        if not chunks:
            return
        embeddings = self._embedder.embed_documents(chunks)
        ids = [f"{c.doc_id}_{c.index}" for c in chunks]
        metadatas = [{"doc_id": c.doc_id, "heading": c.heading, "index": c.index} for c in chunks]
        texts = [c.text for c in chunks]

        self._collection().add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts,
        )

    def query(self, question: str, top_k: int = 3) -> list[dict]:
        query_embedding = self._embedder.embed_query(question)
        results = self._collection().query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
        docs = []
        if results["documents"]:
            for i, text in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i] if results["metadatas"] else {}
                docs.append({
                    "text": text,
                    "heading": meta.get("heading", ""),
                    "doc_id": meta.get("doc_id", ""),
                    "score": results["distances"][0][i] if results.get("distances") else 0,
                })
        return docs

    def clear(self):
        try:
            self._client.delete_collection("documents")
        except ValueError:
            pass

    def list_docs(self) -> list[str]:
        coll = self._collection()
        if coll.count() == 0:
            return []
        results = coll.get(include=["metadatas"])
        seen = set()
        for meta in results["metadatas"]:
            did = meta.get("doc_id", "")
            if did:
                seen.add(did)
        return list(seen)
