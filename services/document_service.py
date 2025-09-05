from config import supabase

TABLE_NAME = "documents"

def get_all_documents():
    response = supabase.table("documents").select("*").execute()
    if response.data:
        return response.data
    return []

def get_documents_by_service_tag(service_tag: str):
    response = supabase.table("documents").select("*").eq("service_tag", service_tag).execute()
    if response.data:
        return response.data
    return []

def delete_document_by_filename(filename: str):
    response = supabase.table(TABLE_NAME).delete().eq("filename", filename).execute()
    if response.data:
        return response.data
    return []

def delete_document_by_id(document_id: str):
    response = supabase.table(TABLE_NAME).delete().eq("id", document_id).execute()
    if response.data:
        return response.data
    return []
