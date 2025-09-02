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
    
def get_monthly_analytics_db():
    try:
        # Ambil semua session dan message
        sessions = supabase.table("chat_sessions").select("id", "created_at").execute().data or []
        messages = supabase.table("chat_messages").select("id", "created_at").execute().data or []

        # Group by bulan
        sessions_month = {}
        for s in sessions:
            month = datetime.fromisoformat(s["created_at"]).strftime("%Y/%m")
            sessions_month[month] = sessions_month.get(month, 0) + 1

        messages_month = {}
        for m in messages:
            month = datetime.fromisoformat(m["created_at"]).strftime("%Y/%m")
            messages_month[month] = messages_month.get(month, 0) + 1

        # Gabungkan bulan dan batasi limit
        all_months = sorted(set(sessions_month.keys()) | set(messages_month.keys()), reverse=True)
        result = []
        for month in all_months:
            result.append({
                "month": month,
                "sessions": sessions_month.get(month, 0),
                "messages": messages_month.get(month, 0)
            })
        return result
    except Exception as e:
        raise Exception(f"Failed to get monthly analytics: {str(e)}")
    
def get_monthly_daily_sessions_db(month: str) -> List[Dict[str, Any]]:
    try:
        # Filter session pada bulan tertentu
        sessions = supabase.table("chat_sessions").select("id", "created_at").execute().data or []
        daily_report = {}
        for session in sessions:
            dt = datetime.fromisoformat(session["created_at"])
            session_month = dt.strftime("%Y/%m")
            if session_month == month:
                day = dt.strftime("%d")
                daily_report[day] = daily_report.get(day, 0) + 1
        # Urutkan hari
        result = [{"day": k, "total_sessions": v} for k, v in sorted(daily_report.items())]
        return result
    except Exception as e:
        raise Exception(f"Failed to get daily sessions for month {month}: {str(e)}")