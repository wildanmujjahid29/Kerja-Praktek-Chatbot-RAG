from datetime import datetime
from typing import Optional, List
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

class KnowledgeInput(BaseModel):
    title: Optional[str] = None
    content: str
    service_tag: Optional[str] = None
    
class DocumentChunkUpdateRequest(BaseModel):
    content: str
    service_tag: Optional[str] = None
    
class DocumentChunkUpdateResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    service_tag: Optional[str]
    content: str
    length: int
    
class ChunkUpdateItem(BaseModel):
    id: str
    content: str
    service_tag: Optional[str] = None

class ChunkBatchUpdateRequest(BaseModel):
    items: List[ChunkUpdateItem]

class ChunkBatchUpdateResponse(BaseModel):
    updated: List[DocumentChunkUpdateResponse]
    total_updated: int