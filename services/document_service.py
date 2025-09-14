from config import supabase

TABLE_NAME = "documents"

def get_all_documents():
    response = supabase.table(TABLE_NAME).select("*").execute()
    if response.data:
        return response.data
    return []

def get_documents_by_service_tag(service_tag: str = None):
    if service_tag is None or service_tag.lower() in ["null", "none", "empty", ""]:
        response = supabase.table(TABLE_NAME).select("*").is_("service_tag", None).execute()
    else:
        response = supabase.table(TABLE_NAME).select("*").eq("service_tag", service_tag).execute()
    
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

def update_document_tag_by_filename(filename: str, service_tag: str = None):
    response = supabase.table(TABLE_NAME).update({"service_tag": service_tag}).eq("filename", filename).execute()
    if response.data:
        return response.data
    return []

def remove_tag_from_document_by_filename(filename: str):
    response = supabase.table(TABLE_NAME).update({"service_tag": None}).eq("filename", filename).execute()
    if response.data:
        return response.data
    return []

def get_unique_service_tags():
    response = supabase.table(TABLE_NAME).select("service_tag").execute()
    if response.data:
        unique_tags = list(set([doc["service_tag"] for doc in response.data if doc["service_tag"] is not None]))
        return unique_tags
    return []
