from config import supabase

TABLE_NAME = "restricted_topics"

def create_topic_db(prompt_id: str, topic: str, enabled: bool = True):
    data = {"prompt_id": prompt_id, "topic": topic, "enabled": enabled}
    result = supabase.table(TABLE_NAME).insert(data).execute()
    return result.data[0] if result.data else None
    
def get_topics_db(prompt_id: str):
    result = supabase.table(TABLE_NAME).select("*").eq("prompt_id", prompt_id).execute()
    return result.data if result.data else []

def get_active_topics_db(prompt_id: str):
    # Return only enabled topics
    result = supabase.table(TABLE_NAME).select("*").eq("prompt_id", prompt_id).eq("enabled", True).execute()
    return result.data if result.data else []

def update_topic_db(topic_id: str, update_data: dict):
    result = supabase.table(TABLE_NAME).update(update_data).eq("id", topic_id).execute()
    return result.data[0] if result.data else None

def toggle_all_topics_db(prompt_id: str, enabled: bool):
    result = supabase.table(TABLE_NAME).update({"enabled": enabled}).eq("prompt_id", prompt_id).execute()
    return result.data if result.data else []

def delete_topic_db(topic_id: str):
    result = supabase.table(TABLE_NAME).delete().eq("id", topic_id).execute()
    return result.data[0] if result.data else None