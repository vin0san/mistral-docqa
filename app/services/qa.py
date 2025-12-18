from typing import Dict, Any, List

from app.core.mistral_client import MistralService
from app.services.embeddings import EmbeddingService
from app.services.retriever import VectorRetriever
from app.services.evaluator import Evaluator


SYSTEM_PROMPT = """You are an expert assistant that provides accurate and concise answers based on the provided context.
Use only the information given in the context to answer the question.
If the answer is not present in the context, say you do not know.
"""


class QAPipeline:
    """
    Retrieval-Augmented Generation (RAG) pipeline.
    """

    def __init__(
        self,
        mistral_service: MistralService,
        embedding_service: EmbeddingService,
        retriever: VectorRetriever,
        evaluator: Evaluator | None = None,
        top_k: int = 3,
    ):
        self.mistral = mistral_service
        self.embedder = embedding_service
        self.retriever = retriever
        self.evaluator = evaluator
        self.top_k = top_k

    def _build_context(self, retrieved_chunks: List[str]) -> str:
        return "\n\n".join(
            f"[Context {i+1}]\n{chunk}"
            for i, chunk in enumerate(retrieved_chunks)
        )

    def answer(self, question: str) -> Dict[str, Any]:
        # 1. Embed query
        query_embedding = self.embedder.embed_texts([question])[0]

        # 2. Retrieve relevant chunks
        results = self.retriever.search(query_embedding, top_k=self.top_k)
        retrieved_chunks = [chunk for chunk, _ in results]

        if not retrieved_chunks:
            return {
                "answer": "I do not know.",
                "context": [],
                "latency_ms": 0.0,
                "usage": {},
            }

        # 3. Build context
        context = self._build_context(retrieved_chunks)

        # 4. Build user prompt
        user_prompt = f"""
Context:
{context}

Question:
{question}

Answer:
""".strip()

        # 5. Call LLM
        response = self.mistral.chat_completion(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        # 6. Record metrics
        if self.evaluator:
            self.evaluator.record(
                latency_ms=response["latency_ms"],
                usage=response["usage"],
            )

        return {
            "answer": response["text"],
            "context": retrieved_chunks,
            "latency_ms": response["latency_ms"],
            "usage": response["usage"],
        }
