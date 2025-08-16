from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List

from .schemas import IngestRequest, AskRequest, Paper, Answer
from .ingest import ingest_query
from .db import get_collection
from .rag import embed_texts, generate_answer

load_dotenv()

app = FastAPI(title="AI Research Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://localhost:{p}" for p in range(5173, 5180)] + ["http://localhost:8501", "http://127.0.0.1:8501", "http://127.0.0.1:8510"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ingest")
def ingest(req: IngestRequest):
    try:
        n = ingest_query(req.query, req.max_results)
        return {"ingested": n}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/ask", response_model=Answer)
def ask(req: AskRequest):
    col = get_collection()
    if col.count() == 0:
        raise HTTPException(400, "No data. Ingest first.")

    q_emb = embed_texts([req.question])[0]
    res = col.query(query_embeddings=[q_emb], n_results=max(1, min(req.k, 10)))

    raw_metas = res["metadatas"][0]
    metas = []
    for m in raw_metas:
        # Rebuild authors list from the stored scalar string
        authors = [a.strip() for a in m.get("authors_str", "").split(",") if a.strip()]
        metas.append(
            {
                "id": m.get("id", ""),
                "title": m.get("title", ""),
                "authors": authors,  # <- list restored for response & prompting
                "summary": m.get("summary", ""),
                "link": m.get("link", ""),
                "published": m.get("published", ""),
            }
        )

    answer = generate_answer(req.question, metas)
    sources = [Paper(**m) for m in metas]
    return Answer(answer=answer, sources=sources)

@app.get("/healthz")
def health():
    return {"ok": True}
