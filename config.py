import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

# Supabase client
supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_ANON_KEY")
    )
