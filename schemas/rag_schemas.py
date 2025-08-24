from pydantic import BaseModel
from typing import Optional

class RAGRequest(BaseModel):
    query: str
    k: Optional[int] = 4
    min_similarity: Optional[float] = 0.5