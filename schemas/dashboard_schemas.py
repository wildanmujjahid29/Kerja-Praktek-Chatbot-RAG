from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class OverviewStats(BaseModel):
    total_services: int
    total_documents: int
    total_chat_sessions: int
    total_user_messages: int
    today_sessions: int
    today_user_messages: int

class ServiceStats(BaseModel):
    service_id: str
    service_name: str
    description: str
    total_documents: int
    total_sessions: int
    total_messages: int
    
class MonthlyAnalyticsItem(BaseModel):
    month: str 
    sessions: int
    messages: int

class MonthlyAnalyticsResponse(BaseModel):
    items: List[MonthlyAnalyticsItem]