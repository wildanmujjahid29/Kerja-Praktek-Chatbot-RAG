from config import supabase

TABLE_NAME = "primary_prompts"

def create_prompt_db(service_id: str, prompt: str):
    data = {"service_id": service_id, "prompt": prompt}
    result = supabase.table(TABLE_NAME).insert(data).execute()
    return result.data[0] if result.data else None

def get_prompt_db(service_id: str):
    result = supabase.table(TABLE_NAME).select("*").eq("service_id", service_id).execute()
    return result.data[0] if result.data else None

def update_prompt_db(prompt_id: str, update_data: dict):
    result = supabase.table(TABLE_NAME).update(update_data).eq("id", prompt_id).execute()
    return result.data[0] if result.data else None

def delete_prompt_db(prompt_id: str):
    result = supabase.table(TABLE_NAME).delete().eq("id", prompt_id).execute()
    return result.data[0] if result.data else None
