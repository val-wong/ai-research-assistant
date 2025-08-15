from typing import List, Dict
from .arxiv_client import search_arxiv
from .db import get_collection
from .rag import embed_texts

def ingest_query(query: str, max_results: int = 20) -> int:
    papers = search_arxiv(query, max_results)
    col = get_collection()
    ids, docs, metas = [], [], []
    for p in papers:
        ids.append(p["id"])
        docs.append(p["title"] + "\n\n" + p["summary"])
        metas.append(p)
    embeddings = embed_texts(docs)
    col.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=embeddings)
    return len(papers)
