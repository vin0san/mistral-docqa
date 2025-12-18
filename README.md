# MistralDocQA

MistralDocQA is a lightweight **Document Question Answering (RAG)** application built using **FastAPI** and **Mistral AI models**.  
It demonstrates how to build clean, testable, developer-friendly AI tooling around LLMs, with a focus on **engineering best practices** rather than UI complexity.

This project was built as part of an internship application and demonstrates engineering-focused LLM system design.

---

## ✨ Features

- 📄 Upload text-based documents (`.txt`, `.md`)
- ✂️ Chunk documents with overlap for better retrieval
- 🧠 Generate embeddings using Mistral embedding models
- 🔍 Perform similarity search using FAISS
- 💬 Answer questions using Retrieval-Augmented Generation (RAG)
- 📊 Track developer-facing metrics (latency, token usage)
- 🧪 Easy to test via Swagger UI or curl

---

## 🏗️ Architecture Overview

```text
      ┌────────────┐
      │   Client   │
      └─────┬──────┘
            │
     FastAPI Routes
            │
    ┌───────▼────────┐
    │   QAPipeline   │
    │ (RAG Orches.)  │
    └───────┬────────┘
            │
┌───────────┼────────────┐
│           │            │
Embeddings Vector Store Evaluator
(Mistral) (FAISS) (Metrics)
```

The design intentionally separates:
- **API layer** (FastAPI routes)
- **Application logic** (RAG pipeline)
- **Infrastructure concerns** (LLM client, config)
- **Developer tooling** (evaluation metrics)

---

## 📂 Project Structure

```bash
mistral-docqa/
├── app/
│ ├── api/ # FastAPI routes
│ ├── core/ # Config & Mistral SDK wrapper
│ ├── services/ # Chunking, retrieval, QA, evaluator
│ ├── models/ # Pydantic schemas
│ └── main.py # App entrypoint
├── tests/ # Unit tests for core logic
├── .env.example
├── README.md
└── requirements.txt
```
---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone <repo-url>
cd mistral-docqa
```
### 2️⃣ Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install dependencies
`pip install -r requirements.txt`

---

## 🔑 API Key Configuration

This project requires a Mistral API key for LLM-related endpoints.

1. Copy the example env file:

`cp .env.example .env`


2. Add your API key:

`MISTRAL_API_KEY=sk-xxxxxxxxxxxxxxxx`


### ⚠️ Important Note:
The application starts without an API key, but `/upload` and `/ask` will raise a clear error if the key is missing.

---
## ▶️ Running the Application

`uvicorn app.main:app --reload`

Open Swagger UI:

`http://127.0.0.1:8000/docs`

---
## 📡 API Endpoints

### 1. `POST /upload`

Upload and index a document.

- Supported formats: `.txt`, `.md`

Example:
```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "file=@example.txt"
```

Response:

`{ "chunks_indexed": 12 }`

### 2. `POST /ask`

Ask a question over the uploaded document.

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this document about?",
    "top_k": 3
  }'
```

Response:
```bash
{
  "answer": "...",
  "context": [...],
  "latency_ms": 412.3,
  "usage": { ... }
}
```
### 3. `GET /metrics`

Developer-facing metrics.

```bash
{
  "total_queries": 5,
  "avg_latency_ms": 380.1,
  "avg_tokens": 210.4
}
```
### 4. `GET /health`

Health check endpoint.

## 🧪 Testing

Run unit tests:

`pytest`


Tests focus on:

* Chunking logic

* Vector retrieval

* RAG pipeline orchestration

* LLM calls are mocked where appropriate to keep tests deterministic.

## 🧠 Design Decisions

* FastAPI chosen for clarity, type-safety, and rapid prototyping of AI tooling.

* Lazy initialization of external services avoids import-time failures and supports reloadable dev servers.

* Dictionary-based LLM messages avoid tight coupling with SDK internals.

* In-memory storage keeps the demo simple and focused on architecture.

* Minimal evaluator demonstrates developer instrumentation without overengineering.

## ⚠️ Limitations

* Embeddings are stored in-memory (no persistence).

* Designed for single-user / demo usage.

* No authentication or rate limiting.

## 🚀 Future Improvements

* Persistent vector storage

* Multi-document support

* PDF ingestion

* Evaluation UI/dashboard

* Async batch embedding

## 📌 Summary

This project focuses on **clean engineering**, **testability**, and **clear separation of concerns** when building LLM-powered applications.
It is intentionally minimal, readable, and easy to extend.