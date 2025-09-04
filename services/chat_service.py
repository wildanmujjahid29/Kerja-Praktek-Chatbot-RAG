import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from config import supabase
from schemas.chat_schemas import (ChatMessage, ChatSession,
                                    ChatSessionWithMessages)
from services.rag_service import run_rag

CHAT_SESSIONS = "chat_sessions"
CHAT_MESSAGES = "chat_messages"


def create_session(user_id: str, service_id: str, session_name: str = "New Chat") -> ChatSession:
    # Ambil nama service dari database
    service_result = supabase.table("services").select("name").eq("id", service_id).single().execute()
    service_name = service_result.data["name"] if service_result.data else ""
    # Gabungkan ke session_name
    session_name_full = f"{session_name} - {service_name}" if service_name else session_name
    data = {"user_id": user_id, "service_id": service_id, "session_name": session_name_full}
    result = supabase.table(CHAT_SESSIONS).insert(data).execute()
    if not result.data:
        raise Exception("Failed to create chat session")
    return ChatSession(**result.data[0])

def get_session_with_messages(session_id: str) -> ChatSessionWithMessages:
    
    # Get session data
    session_result = supabase.table(CHAT_SESSIONS).select("*").eq("id", session_id).single().execute()
    session_data = session_result.data
    if not session_data:
        raise Exception("Chat session not found")
    
    # Get messages for the session
    messages_result = supabase.table(CHAT_MESSAGES).select("*").eq("session_id", session_id).order("created_at").execute()
    messages_data = messages_result.data or []
    messages = [ChatMessage(**msg) for msg in messages_data]
    return ChatSessionWithMessages(**session_data, messages=messages)

def list_sessions_by_service(user_id: str, service_id: str) -> List[ChatSession]:
    result = supabase.table(CHAT_SESSIONS).select("*").eq("user_id", user_id).eq("service_id", service_id).eq("is_active", True).order("updated_at", desc=True).execute()

    sessions_data = result.data or []
    return [ChatSession(**session) for session in sessions_data]


def list_sessions_by_user(user_id: str) -> List[ChatSession]:
    result = supabase.table(CHAT_SESSIONS).select("*").eq("user_id", user_id).eq("is_active", True).order("updated_at", desc=True).execute()

    sessions_data = result.data or []
    return [ChatSession(**session) for session in sessions_data]

def save_message(session_id: str, role: str, content: str, sources: List[Dict] = None) -> ChatMessage:
    data = {
        "session_id": session_id,
        "role": role,
        "content": content,
        "sources": sources
    }
    result = supabase.table(CHAT_MESSAGES).insert(data).execute()
    message_data = result.data[0]
    
    supabase.table(CHAT_SESSIONS).update({"updated_at": datetime.utcnow().isoformat()}).eq("id", session_id).execute()

    return ChatMessage(**message_data)

def send_message(session_id: str, user_message: str, k: int = 3, min_similarity: float = 0.3) -> Dict[str, Any]:
    # Get session to get service_id
    session = get_session_with_messages(session_id)
    
    # Save user message
    user_msg = save_message(session_id, "user", user_message)
    
    # Get RAG result
    print(f"DEBUG chat_service: Calling run_rag with service_id={session.service_id}, query='{user_message}'")
    rag_result = run_rag(
        service_id=session.service_id,
        query=user_message,
        k=k,
        min_similarity=min_similarity
    )
    print(f"DEBUG chat_service: RAG result = {rag_result}")

    # Save RAG result
    assistant_msg = save_message(session_id, "assistant", rag_result["answer"], rag_result.get("sources", []))
    
    return {
        "session_id": session_id,
        "user_message": user_msg,
        "assistant_message": assistant_msg,
        "rag_metadata": {
            # "used_k": rag_result["used_k"],
            "sources": rag_result["sources"]
        }
    }
    
def delete_session(session_id: str) -> bool:
    try:
        supabase.table(CHAT_SESSIONS).update({"is_active": False}).eq("id", session_id).execute()
        return True
    except Exception as e:
        raise Exception(f"Failed to delete session: {str(e)}")