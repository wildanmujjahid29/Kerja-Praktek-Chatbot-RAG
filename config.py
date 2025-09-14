import os

from dotenv import load_dotenv
from supabase import Client, create_client
from functools import lru_cache

load_dotenv()

# Supabase client
supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_ANON_KEY")
    )

# Api key AI
@lru_cache(maxsize=1)
def get_api_key():
    response = supabase.table("configurations").select("value").eq("key", "api_key").single().execute()
    if response.data:
        return response.data['value']
    return None

def refresh_api_key():
    get_api_key.cache_clear()
