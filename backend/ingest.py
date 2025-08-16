from typing import List, Dict
from .arxiv_client import search_arxiv
from .db import get_collection
from .rag import embed_texts

def ingest_query(query: str, max_results: int = 20) -> int:
    """
    Fetch papers from arXiv and index them into Chroma.
    NOTE: Chroma metadata must be scalars (str/int/float/bool/None),
    so we store authors as a single string 'authors_str'.
    """
    papers = search_arxiv(query, max_results)
    col = get_collection()

    ids, docs, metas = [], [], []
    for p in papers:
        pid = p["id"]
        title = p["title"]
        summary = p["summary"]
        authors_str = ", ".join(p.get("authors", []))  # <-- flatten list

        ids.append(pid)
        docs.append(f"{title}\n\n{summary}")
        metas.append(
            {
                "id": pid,
                "title": title,
                "summary": summary,
                "link": p.get("link", ""),
                "published": p.get("published", ""),
                "authors_str": authors_str,  # <-- scalar only
            }
        )

    embeddings = embed_texts(docs)
    col.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=embeddings)
    return len(papers)
