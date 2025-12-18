from typing import List, Optional
from pydantic import BaseModel

class UploadResponse(BaseModel):
    chunks_indexed: int

class AskRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3

class AskResponse(BaseModel):
    answer: str
    context: List[str]
    latency_ms: float
    usage: dict