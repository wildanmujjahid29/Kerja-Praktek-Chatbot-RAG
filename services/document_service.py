from config import supabase
from services.embed_service import embeddings, preprocess_text, normalize_vector

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

def get_document_chunk_by_id(document_id: str):
    response = supabase.table(TABLE_NAME).select("*").eq("id", document_id).execute()
    if response.data and len(response.data) > 0:
        return response.data[0]
    return None

def update_document_chunk(document_id: str, new_content: str, new_service_tag: str | None = None):
    # Ambil dulu row
    row = get_document_chunk_by_id(document_id)
    if not row:
        return None
    
    # Preprocess & embed ulang
    processed = preprocess_text(new_content)
    vector = embeddings.embed_documents([processed])[0]
    vector = normalize_vector(vector)

    update_data = {
        "content": processed,
        "embedding": vector
    }
    if new_service_tag is not None:  # hanya update kalau dikirim
        update_data["service_tag"] = new_service_tag

    resp = supabase.table(TABLE_NAME).update(update_data).eq("id", document_id).execute()
    if resp.data and len(resp.data) > 0:
        updated = resp.data[0]
        # bentuk response ringkas
        return {
            "id": updated["id"],
            "filename": updated["filename"],
            "file_type": updated["file_type"],
            "service_tag": updated.get("service_tag"),
            "content": updated["content"],
            "length": len(updated["content"])
        }
    return None

def update_document_chunks_batch(items: list[dict]):
    results = []
    for item in items:
        chunk_id = item["id"]
        content = item["content"]
        service_tag = item.get("service_tag", None)
        updated = update_document_chunk(chunk_id, content, service_tag)
        if updated:
            results.append(updated)
    return results