from config import supabase

TABLE_NAME = "services"

def create_service_db(name: str, description: str):
    data = {"name": name, "description": description}
    result = supabase.table(TABLE_NAME).insert(data).execute()
    return result.data[0] if result.data else None

def get_all_services_db():
    result = supabase.table(TABLE_NAME).select("*").execute()
    return result.data if result.data else []

def get_service_by_id_db(service_id: str):
    result = supabase.table(TABLE_NAME).select("*").eq("id", service_id).single().execute()
    return result.data if result.data else None

def update_service_db(service_id: str, data: dict):
    result = supabase.table(TABLE_NAME).update(data).eq("id", service_id).execute()
    return result.data[0] if result.data else None

def delete_service_db(service_id: str):
    result = supabase.table(TABLE_NAME).delete().eq("id", service_id).execute()
    return result.data[0] if result.data else None
