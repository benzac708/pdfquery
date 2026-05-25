from ccep.config import COHERE_API_KEY, EMBEDDING_PROVIDER
from ccep.models import Chunk


class Embedder:
    def __init__(self):
        self._model = None
        self._co = None
        self._provider = EMBEDDING_PROVIDER

    def _get_cohere(self):
        if self._co is None:
            import cohere
            self._co = cohere.ClientV2(api_key=COHERE_API_KEY)
        return self._co

    def _get_local(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        return self._model

    def embed_documents(self, chunks: list[Chunk]) -> list[list[float]]:
        texts = [c.text for c in chunks]
        if self._provider == "cohere" and COHERE_API_KEY:
            return self._embed_cohere(texts, "search_document")
        return self._embed_local(texts)

    def embed_query(self, text: str) -> list[float]:
        if self._provider == "cohere" and COHERE_API_KEY:
            return self._embed_cohere([text], "search_query")[0]
        return self._embed_local([text])[0]

    def _embed_cohere(self, texts: list[str], input_type: str) -> list[list[float]]:
        co = self._get_cohere()
        resp = co.embed(
            texts=texts,
            model="embed-multilingual-v3.0",
            input_type=input_type,
        )
        floats = resp.embeddings.float_
        if floats is not None:
            return floats
        ints = resp.embeddings.int8
        if ints is not None:
            return [[float(v) for v in vec] for vec in ints]
        uints = resp.embeddings.uint8
        return [[float(v) for v in vec] for vec in uints]

    def _embed_local(self, texts: list[str]) -> list[list[float]]:
        model = self._get_local()
        return model.encode(texts).tolist()
