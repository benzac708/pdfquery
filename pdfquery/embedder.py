from pdfquery.config import COHERE_API_KEY
from pdfquery.models import Chunk


class Embedder:
    def __init__(self):
        self._co = None

    def _get_cohere(self):
        if self._co is None:
            import cohere
            self._co = cohere.ClientV2(api_key=COHERE_API_KEY)
        return self._co

    def embed_documents(self, chunks: list[Chunk]) -> list[list[float]]:
        texts = [c.text for c in chunks]
        return self._embed(texts, "search_document")

    def embed_query(self, text: str) -> list[float]:
        return self._embed([text], "search_query")[0]

    def _embed(self, texts: list[str], input_type: str) -> list[list[float]]:
        co = self._get_cohere()
        resp = co.embed(
            texts=texts,
            model="embed-multilingual-v3.0",
            input_type=input_type,
        )
        if resp.embeddings.float_ is not None:
            return resp.embeddings.float_
        if resp.embeddings.int8 is not None:
            return [[float(v) for v in vec] for vec in resp.embeddings.int8]
        return [[float(v) for v in vec] for vec in resp.embeddings.uint8]
