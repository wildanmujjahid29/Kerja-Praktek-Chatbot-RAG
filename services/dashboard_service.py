from datetime import datetime, timedelta
from typing import Any, Dict, List

from config import supabase


def get_overview_stats_db() -> Dict[str, Any]:
    """
    Mengembalikan statistik global:
    - Total dokumen unik yang diunggah
    - Total sesi chat
    - Total pesan user
    - Jumlah sesi chat hari ini
    - Jumlah pesan user hari ini
    """
    try:
        # Total Documents
        documents = supabase.table("documents").select("filename").execute()
        unique_documents = {doc["filename"] for doc in documents.data}
        total_documents = len(unique_documents)

        # Total Chat Sessions
        chat_sessions = supabase.table("chat_sessions").select("id", count="exact").execute()
        total_chat_sessions = chat_sessions.count or 0

        # Total User Messages
        messages = supabase.table("chat_messages").select("id", count="exact").eq("role", "user").execute()
        total_user_messages = messages.count or 0

        # Today Sessions
        today = datetime.utcnow().date()
        today_sessions_result = supabase.table("chat_sessions").select("id", count="exact").gte("created_at", today.isoformat()).execute()
        today_sessions = today_sessions_result.count or 0

        # Today User Messages
        today_messages_result = supabase.table("chat_messages").select("id", count="exact").eq("role", "user").gte("created_at", today.isoformat()).execute()
        today_user_messages = today_messages_result.count or 0

        return {
            "total_documents": total_documents,
            "total_chat_sessions": total_chat_sessions,
            "total_user_messages": total_user_messages,
            "today_sessions": today_sessions,
            "today_user_messages": today_user_messages,
        }
    except Exception as e:
        raise Exception(f"Failed to get overview stats: {str(e)}")
    
## Fungsi statistik per service dihapus karena tidak relevan lagi
    
def get_monthly_analytics_db() -> List[Dict[str, Any]]:
    """
    Statistik bulanan: jumlah sesi dan pesan per bulan.
    """
    try:
        sessions = supabase.table("chat_sessions").select("id", "created_at").execute().data or []
        messages = supabase.table("chat_messages").select("id", "created_at").execute().data or []

        sessions_month = {}
        for s in sessions:
            month = datetime.fromisoformat(s["created_at"]).strftime("%Y/%m")
            sessions_month[month] = sessions_month.get(month, 0) + 1

        messages_month = {}
        for m in messages:
            month = datetime.fromisoformat(m["created_at"]).strftime("%Y/%m")
            messages_month[month] = messages_month.get(month, 0) + 1

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
    """
    Statistik harian: jumlah sesi per hari dalam bulan tertentu.
    """
    try:
        sessions = supabase.table("chat_sessions").select("id", "created_at").execute().data or []
        daily_report = {}
        for session in sessions:
            dt = datetime.fromisoformat(session["created_at"])
            session_month = dt.strftime("%Y/%m")
            if session_month == month:
                day = dt.strftime("%d")
                daily_report[day] = daily_report.get(day, 0) + 1
        result = [{"day": k, "total_sessions": v} for k, v in sorted(daily_report.items())]
        return result
    except Exception as e:
        raise Exception(f"Failed to get daily sessions for month {month}: {str(e)}")