import arxiv
from typing import List, Dict

def search_arxiv(query: str, max_results: int = 20) -> List[Dict]:
    results = []
    for r in arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance).results():
        results.append({
            "id": r.entry_id,
            "title": r.title.strip(),
            "authors": [a.name for a in r.authors],
            "summary": r.summary.strip(),
            "link": r.pdf_url or r.entry_id,
            "published": r.published.strftime("%Y-%m-%d")
        })
    return results
