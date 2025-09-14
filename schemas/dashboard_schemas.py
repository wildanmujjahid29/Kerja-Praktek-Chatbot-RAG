from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class OverviewStats(BaseModel):
    total_documents: int
    total_chat_sessions: int
    total_user_messages: int
    today_sessions: int
    today_user_messages: int


class MonthlyAnalyticsItem(BaseModel):
    month: str 
    sessions: int
    messages: int

class MonthlyAnalyticsResponse(BaseModel):
    items: List[MonthlyAnalyticsItem]