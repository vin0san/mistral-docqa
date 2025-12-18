class DummyMistral:
    def chat_completion(self, system_prompt, user_prompt, temperature=0.2):
        return {
            "text": "mock answer",
            "latency_ms": 10.0,
            "usage": {"total_tokens": 10},
        }


class DummyEmbedder:
    def embed_texts(self, texts):
        return [[1.0, 0.0, 0.0]]


class DummyRetriever:
    def search(self, query_embedding, top_k=3):
        return [("test chunk", 0.0)]


from app.services.qa import QAPipeline


def test_qa_pipeline():
    qa = QAPipeline(
        mistral_service=DummyMistral(),
        embedding_service=DummyEmbedder(),
        retriever=DummyRetriever(),
    )

    result = qa.answer("What is this?")

    assert result["answer"] == "mock answer"
    assert "test chunk" in result["context"][0]
