from app.services.retriever import VectorRetriever

def test_add_and_search():
    retriever = VectorRetriever(embedding_dim=3)

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]

    chunks = ["A", "B", "C"]
    retriever.add(embeddings, chunks)

    query = retriever.search([1.0, 0.0, 0.0], top_k=1)

    assert len(query) == 1
    assert query[0][0] == "A"