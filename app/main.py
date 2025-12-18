from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Mistral DocQA",
    description="A document question-answering service powered by Mistral AI.",
    version="0.1.0",
)

app.include_router(router)