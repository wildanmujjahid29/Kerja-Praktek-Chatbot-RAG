import uuid
from typing import Optional

from pydantic import BaseModel


class PromptBase(BaseModel):
    prompt: str

class PromptCreate(PromptBase):
    pass

class PromptUpdate(BaseModel):
    prompt: Optional[str] = None

class PromptResponse(PromptBase):
    id: uuid.UUID
    service_id: uuid.UUID
