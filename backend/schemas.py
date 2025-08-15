from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    query: str
    max_results: int = 20

class AskRequest(BaseModel):
    question: str
    k: int = 5

class Paper(BaseModel):
    id: str
    title: str
    authors: List[str]
    summary: str
    link: str
    published: str

class Answer(BaseModel):
    answer: str
    sources: List[Paper]
