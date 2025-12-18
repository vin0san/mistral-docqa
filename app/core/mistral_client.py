import time
from typing import List, Dict, Any, Optional

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
        self._client: Optional[MistralClient] = None

    def _get_client(self) -> MistralClient:
        if not settings.MISTRAL_API_KEY:
            raise RuntimeError(
                "MISTRAL_API_KEY is not set. Please configure it via environment variables or .env file."
            )

        if self._client is None:
            self._client = MistralClient(api_key=settings.MISTRAL_API_KEY)

        return self._client

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        """
        client = self._get_client()

        response = client.embeddings.create(
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
        client = self._get_client()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        start = time.perf_counter()

        response = client.chat.complete(
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
