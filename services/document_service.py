from config import supabase

TABLE_NAME = "documents"

def get_documents_by_service(service_id: str):
    response = supabase.table("documents").select("*").eq("service_id", service_id).execute()
    if response.data:
        return response.data
    return []

def delete_document_by_filename(service_id: str, filename: str):
    response = supabase.table(TABLE_NAME).delete().eq("service_id", service_id).eq("filename", filename).execute()
    if response.data:
        return response.data
    return []
