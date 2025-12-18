from typing import List
from app.core.mistral_client import MistralService

class EmbeddingService:
    """
    Service for generating embeddings using Mistral AI.
    """

    def __init__(self, mistral_service: MistralService):
        self.mistral = mistral_service

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        
        return self.mistral.embed(texts)