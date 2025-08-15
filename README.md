# AI Research Assistant (RAG on arXiv)

## Features
- Search and ingest arXiv papers
- Vector search (Chroma)
- Answer questions with citations
- Switchable embeddings/LLM: OpenAI or local

## Setup
```bash
git clone <your-repo-url>
cd ai-research-assistant
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

Backend
uvicorn backend.main:app --reload

Frontend
cd frontend
streamlit run app.py

Open http://localhost:8501

Typical Flow
Ingest: use a focused arXiv query (e.g., retrieval augmented generation evaluation)

Ask: prompt the question; adjust Top-K

Show answer and sources

Notes
Local mode uses all-MiniLM-L6-v2 for embeddings and a simple extractive fallback answer.

For better answers, set USE_OPENAI=true and specify LLM_MODEL and EMBED_MODEL.

Data persists in .chroma/.


---

# how to run (quickstart)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# add your OPENAI_API_KEY if you want OpenAI; else set USE_OPENAI=false
uvicorn backend.main:app --reload
# in another terminal
streamlit run frontend/app.py
