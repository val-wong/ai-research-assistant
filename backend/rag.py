import os
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
from openai import OpenAI

_model = None
_openai = None

def get_embedder():
    global _model, _openai
    use_openai = os.getenv("USE_OPENAI", "true").lower() == "true"
    if use_openai:
        if _openai is None:
            _openai = OpenAI()
        return ("openai", os.getenv("EMBED_MODEL", "text-embedding-3-small"))
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return ("local", _model)

def embed_texts(texts: List[str]) -> List[List[float]]:
    kind, obj = get_embedder()
    if kind == "openai":
        resp = OpenAI().embeddings.create(model=obj, input=texts)
        return [d.embedding for d in resp.data]
    return obj.encode(texts, normalize_embeddings=True).tolist()

def build_prompt(question: str, contexts: List[Dict]) -> str:
    ctx = ""
    for i, c in enumerate(contexts, 1):
        ctx += f"[{i}] Title: {c['title']}\nAuthors: {', '.join(c['authors'])}\nPublished: {c['published']}\nLink: {c['link']}\nAbstract: {c['summary']}\n\n"
    return f"Answer the question using only the context. Cite sources as [1], [2], etc.\n\nContext:\n{ctx}\nQuestion: {question}\nAnswer:"

def generate_answer(question: str, contexts: List[Dict]) -> str:
    use_openai = os.getenv("USE_OPENAI", "true").lower() == "true"
    if use_openai:
        model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        client = OpenAI()
        msg = [{"role":"system","content":"You are a precise research assistant."},
               {"role":"user","content":build_prompt(question, contexts)}]
        r = client.chat.completions.create(model=model, messages=msg, temperature=0.2)
        return r.choices[0].message.content.strip()
    text = "\n\n".join([c["summary"] for c in contexts])
    return text[:1200]
