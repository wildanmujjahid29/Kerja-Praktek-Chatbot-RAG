from config import supabase
from config import refresh_api_key

TABLE_NAME = "configurations"

def get_config_db():
    response = supabase.table(TABLE_NAME).select("value").eq("key", "api_key").single().execute()
    if response.data:
        return {"api_key": response.data['value']}
    return None

def set_config_db(value: str):
    response = supabase.table(TABLE_NAME).upsert({"key": "api_key", "value": value}).execute()
    refresh_api_key()
    return response.data
