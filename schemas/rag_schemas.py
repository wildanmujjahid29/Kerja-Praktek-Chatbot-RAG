from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class RAGRequest(BaseModel):
    query: str

class RAGSource(BaseModel):
    index: int
    filename: str
    similarity: float

class RAGResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]] = []
    used_k: int = 0
    query: str
    is_fallback: bool = False
    is_restricted_topic: bool = False