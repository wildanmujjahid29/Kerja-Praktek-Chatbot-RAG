from pydantic import BaseModel


class RestrictedTopicBase(BaseModel):
    topic: str
    enabled: bool = True
    
class RestrictedTopicCreate(RestrictedTopicBase):
    prompt_id: str
    
class RestrictedTopicResponse(RestrictedTopicBase):
    id: str
    prompt_id: str
