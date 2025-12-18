from typing import List, Tuple
import numpy as np
import faiss


class VectorRetriever:
    """
    Stores embeddings and retrieves top-k similar chunks.
    """

    def __init__(self, embedding_dim: int):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.text_chunks: List[str] = []

    def add(self, embeddings: List[List[float]], chunks: List[str]) -> None:
        if len(embeddings) != len(chunks):
            raise ValueError("Embeddings and chunks must be same length")

        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.text_chunks.extend(chunks)

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Tuple[str, float]]:
        if self.index.ntotal == 0:
            return []

        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1:
                continue
            results.append((self.text_chunks[idx], float(dist)))

        return results
