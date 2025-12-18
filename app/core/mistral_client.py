import time
from typing import List, Dict, Any

from mistralai.client import MistralClient
from app.core.config import settings


class MistralService:
    """
    Thin wrapper around the Mistral AI client.

    Responsibilities:
    - Chat completions
    - Embeddings
    - Basic instrumentation (latency, token usage)
    """

    def __init__(self):
        if not settings.MISTRAL_API_KEY:
            raise RuntimeError("MISTRAL_API_KEY is not set")

        self.client = MistralClient(api_key=settings.MISTRAL_API_KEY)

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        """
        response = self.client.embeddings.create(
            model=settings.EMBEDDING_MODEL,
            input=texts,
        )

        return [item.embedding for item in response.data]

    def chat_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
        """
        Generate chat completion with basic metrics.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        start = time.perf_counter()

        response = self.client.chat.complete(
            model=settings.CHAT_MODEL,
            messages=messages,
            temperature=temperature,
        )

        latency_ms = (time.perf_counter() - start) * 1000

        return {
            "text": response.choices[0].message.content,
            "latency_ms": latency_ms,
            "usage": response.usage,
        }
