from pdfquery.config import GROQ_API_KEY, TOP_K
from pdfquery.vectordb import VectorDB
from groq import Groq


class RAG:
    def __init__(self):
        self._db = VectorDB()
        self._client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

    def query(self, question: str) -> dict:
        chunks = self._db.query(question, top_k=TOP_K)
        if not chunks:
            return {"answer": "No documents ingested yet. Upload a PDF first.", "sources": []}

        context = "\n\n".join(f"[{c['heading']}]: {c['text'][:2000]}" for c in chunks)
        prompt = f"""You are a helpful assistant answering questions about uploaded documents. Use the context below as your primary source. If the context doesn't contain enough detail, you may use your general knowledge to supplement, but clearly indicate what comes from the document vs what you're adding.

Context from the document:
{context}

Question: {question}"""

        if self._client:
            resp = self._client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1024,
            )
            answer = resp.choices[0].message.content
        else:
            answer = "[Groq API key not set. Set GROQ_API_KEY to get AI answers.]"

        return {
            "answer": answer,
            "sources": [{"heading": c["heading"], "text": c["text"][:300]} for c in chunks],
        }
