from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EmbedResponse(BaseModel):
    status: str
    filename: str
    file_type: str
    chunks_saved: int

class DocumentOut(BaseModel):
    id: str
    filename: str
    file_type: str
    uploaded_at: datetime

class DocumentTagOut(DocumentOut):
    service_tag: Optional[str] = None

class UpdateTagRequest(BaseModel):
    service_tag: Optional[str] = None

class UniqueTagsResponse(BaseModel):
    tags: list[str] 