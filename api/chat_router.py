from typing import List

from fastapi import APIRouter, HTTPException, Query

from schemas.chat_schemas import (ChatResponse, ChatSession,
                                    ChatSessionWithMessages,
                                    CreateChatSessionRequest, SendMessageRequest)
from services.chat_service import (create_session, delete_session,
                                    get_session_with_messages,
                                    list_sessions_by_user, send_message)

router = APIRouter()

@router.post("/chat/session")
def create_chat_session(request: CreateChatSessionRequest) -> ChatSession:
    try:
        session = create_session(user_id=request.user_id, session_name=request.session_name or "New Chat")
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/session/{session_id}/message")
def send_message_endpoint(session_id: str, request: SendMessageRequest) -> ChatResponse:
    try:
        session = get_session_with_messages(session_id=session_id)
        if not session.is_active:
            raise HTTPException(status_code=403, detail="Session is not active. Cannot send message.")
        result = send_message(
            session_id,
            request.message,
            request.k or 3,
            request.min_similarity or 0.3
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/session/{session_id}")
def get_chat_session(session_id: str) -> ChatSessionWithMessages:
    try:
        session = get_session_with_messages(session_id=session_id)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/sessions/user/{user_id}")
def list_user_sessions(user_id: str) -> List[ChatSession]:
    try:
        sessions = list_sessions_by_user(user_id)
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/chat/session/{session_id}")
def delete_chat_session(session_id: str) -> dict:
    try:
        success = delete_session(session_id)
        return {"status": "success" if success else "failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))