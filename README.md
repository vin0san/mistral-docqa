## Repo Structure

```bash

mistral-docqa/
├── app/
│   ├── main.py                # FastAPI app entrypoint
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # HTTP endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # env vars, settings
│   │   └── mistral_client.py  # Mistral SDK wrapper
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_loader.py # load PDF/TXT
│   │   ├── chunker.py         # chunking strategy
│   │   ├── embeddings.py      # embedding generation
│   │   ├── retriever.py       # similarity search
│   │   ├── qa.py              # RAG pipeline
│   │   └── evaluator.py       # metrics, latency, tokens
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models
│   └── utils/
│       ├── __init__.py
│       └── logging.py
│
├── tests/
│   ├── test_chunker.py
│   ├── test_retriever.py
│   └── test_qa.py
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml             # optional but clean
```

## Architecture

```bash

User
 │
 │  (question)
 ▼
FastAPI
 │
 ├─► Retriever ─► Embeddings ─► Vector Store
 │
 └─► Mistral Chat Model
        ▲
        │
   Retrieved Context
```
