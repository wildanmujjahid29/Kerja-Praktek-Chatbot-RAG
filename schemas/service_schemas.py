from pydantic import BaseModel
from typing import Optional

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = None 
    description: Optional[str] = None

class ServiceResponse(ServiceBase):
    id: str