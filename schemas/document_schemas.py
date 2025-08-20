from datetime import datetime

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
    