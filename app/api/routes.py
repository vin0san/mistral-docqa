from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.mistral_client import MistralService
from app.services.chunker import TextChunker
from app.services.embeddings import EmbeddingService
from app.services.retriever import VectorRetriever
from app.services.qa import QAPipeline
from app.models.schemas import UploadResponse, AskRequest, AskResponse
from app.services.evaluator import Evaluator
from app.services.document_loader import DocumentLoader


router = APIRouter()

# ---- Lazy singletons ----

_mistral_service = None
_embedding_service = None
_retriever = None
_qa_pipeline = None
_chunker = None
_evaluator = None


def get_evaluator():
    global _evaluator
    if _evaluator is None:
        _evaluator = Evaluator()
    return _evaluator


def get_qa_pipeline() -> QAPipeline:
    global _mistral_service, _embedding_service, _retriever, _qa_pipeline, _chunker, _evaluator

    if _qa_pipeline is None:
        _mistral_service = MistralService()
        _embedding_service = EmbeddingService(_mistral_service)

        _retriever = VectorRetriever(embedding_dim=1024)
        _chunker = TextChunker(chunk_size=500, overlap=100)
        _evaluator = get_evaluator()

        _qa_pipeline = QAPipeline(
            mistral_service=_mistral_service,
            embedding_service=_embedding_service,
            retriever=_retriever,
            evaluator=_evaluator,
        )

    return _qa_pipeline


def get_chunker() -> TextChunker:
    global _chunker
    if _chunker is None:
        _chunker = TextChunker(chunk_size=500, overlap=100)
    return _chunker


# ---- Routes ----

@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    qa = get_qa_pipeline()

    content = await DocumentLoader.load(file)

    chunks = get_chunker().chunk(content)
    if not chunks:
        raise HTTPException(status_code=400, detail="Document is empty")

    embeddings = qa.embedder.embed_texts(chunks)
    qa.retriever.add(embeddings, chunks)

    return UploadResponse(chunks_indexed=len(chunks))


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    qa = get_qa_pipeline()

    if qa.retriever.index.ntotal == 0:
        raise HTTPException(status_code=400, detail="No document uploaded yet")

    qa.top_k = request.top_k

    result = qa.answer(request.question)
    return AskResponse(**result)


@router.get("/metrics")
def metrics():
    evaluator = get_evaluator()
    return evaluator.summary()
