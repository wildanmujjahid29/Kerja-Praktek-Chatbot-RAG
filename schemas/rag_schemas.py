from typing import Any, Dict, List

from pydantic import BaseModel, Field


class RAGRequest(BaseModel):
    query: str
    k: int = Field(3, ge=1, le=50, description="Jumlah dokumen teratas yang diambil")
    min_similarity: float = Field(0.4, ge=0.0, le=1.0, description="Ambang batas similarity untuk filter hasil")

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