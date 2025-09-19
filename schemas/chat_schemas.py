from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class ChatMessage(BaseModel):
    id: str
    role: str
    content: str
    sources: Optional[List[Dict]] = None
    created_at : datetime
    
class ChatSession(BaseModel):
    id: str
    user_id: Optional[str] = None
    session_name: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    is_active: bool = True
    
class ChatSessionWithMessages(ChatSession):
    messages: List[ChatMessage] = []
    
class SendMessageRequest(BaseModel):
    message: str
    k: int = 5
    min_similarity: float = 0.3
        
class ChatResponse(BaseModel):
    session_id: str 
    user_message: ChatMessage
    assistant_message: ChatMessage

class SessionResponse(BaseModel):
    session_id: str
    session_name: str
    created_at: datetime
    is_new: bool = False
