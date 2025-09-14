from config import supabase

TABLE_NAME = "primary_prompt"

def create_prompt_db(prompt: str, fallback_response: str = None):
    data = {"prompt": prompt, "fallback_response": fallback_response, "is_active": True}
    result = supabase.table(TABLE_NAME).insert(data).execute()
    return result.data[0] if result.data else None

def get_prompt_db():
    result = supabase.table(TABLE_NAME).select("*").eq("is_active", True).single().execute()
    return result.data if result.data else None

def update_prompt_db(prompt_id: str, update_data: dict):
    result = supabase.table(TABLE_NAME).update(update_data).eq("id", prompt_id).execute()
    return result.data[0] if result.data else None

def delete_prompt_db(prompt_id: str):
    result = supabase.table(TABLE_NAME).update({"is_active": False}).eq("id", prompt_id).execute()
    return result.data[0] if result.data else None
