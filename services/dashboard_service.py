from datetime import datetime, timedelta
from typing import Any, Dict, List

from config import supabase

def get_overview_stats_db() -> Dict[str, Any]:
    try:
        # Total Services
        services = supabase.table("services").select("id", count="exact").execute()
        total_services = services.count or 0
        
        # Total Documents
        documents = supabase.table("documents").select("filename").execute()
        unique_documents = {doc["filename"] for doc in documents.data}
        total_documents = len(unique_documents)
        
        # Total Chat Session
        chat_sessions = supabase.table("chat_sessions").select("id", count="exact").execute()
        total_chat_sessions = chat_sessions.count or 0
        
        # Total Message user
        messages = supabase.table("chat_messages").select("id", count="exact").eq("role", "user").execute()
        total_user_messages = messages.count or 0

        # Today Sessions
        today = datetime.utcnow().date()
        today_sessions_result = supabase.table("chat_sessions").select("id", count="exact").gte("created_at", today.isoformat()).execute()
        today_sessions = today_sessions_result.count or 0

        # Today user message
        today_messages_result = supabase.table("chat_messages").select("id", count="exact").eq("role", "user").gte("created_at", today.isoformat()).execute()
        today_user_messages = today_messages_result.count or 0

        return {
            "total_services": total_services,
            "total_documents": total_documents,
            "total_chat_sessions": total_chat_sessions,
            "total_user_messages": total_user_messages,
            "today_sessions": today_sessions,
            "today_user_messages": today_user_messages,
        }
    except Exception as e:
        raise Exception(f"Failed to get overview stats: {str(e)}")
    
def get_service_stats_db() -> List[Dict[str, Any]]:
    try:
        services_result = supabase.table("services").select("*").execute()
        services = services_result.data or []

        services_stats = []
        
        for service in services:
            service_id = service["id"]
            service_name = service["name"]
            service_description = service["description"]
            
            # Unique document service count
            documents = supabase.table("documents").select("filename").eq("service_id", service_id).execute()
            unique_documents = {doc["filename"] for doc in documents.data}
            unique_document_count = len(unique_documents)

            # Total chat session
            session = supabase.table("chat_sessions").select("id", count="exact").eq("service_id", service_id).execute()
            total_sessions = session.count or 0

            # Total user message
            sessions_ids = [s["id"] for s in supabase.table("chat_sessions").select("id").eq("service_id", service_id).execute().data or []]
            if sessions_ids:
                messages_count = supabase.table("chat_messages").select("id", count="exact").in_("session_id", sessions_ids).eq("role", "user").execute()
                total_user_messages = messages_count.count or 0
            else:
                total_user_messages = 0
    
            services_stats.append({
                "service_id": service_id,
                "service_name": service_name,
                "description": service_description,
                "total_documents": unique_document_count,
                "total_sessions": total_sessions,
                "total_messages": total_user_messages
            })
            
        services_stats.sort(key=lambda x: x["total_sessions"], reverse=True)
        return services_stats
    except Exception as e:
        raise Exception(f"Failed to get service stats: {str(e)}")
    
