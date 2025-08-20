import os
import shutil
import uuid

from fastapi import APIRouter, Form, UploadFile, HTTPException
from schemas.document_schemas import DocumentOut
from services.document_service import get_documents_by_service, delete_document_by_filename
from services.embed_service import embedding_text_from_file
router = APIRouter()


@router.post("/document/embed")
async def embed_file(service_id: str = Form(...), file: UploadFile = None):
    # simpan file sementara
    temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # proses embedding dengan metadata
    result = embedding_text_from_file(service_id, temp_filename, file.filename)

    # hapus file sementara
    os.remove(temp_filename)
    return {
        "status": "success",
        "filename": file.filename,
        "file_type": file.filename.split(".")[-1].lower(),
        "chunks_saved": len(result)
    }

@router.get("/document/{service_id}", response_model=list[DocumentOut])
def list_unique_documents(service_id: str):
    documents = get_documents_by_service(service_id)
    # Filter unik berdasarkan filename
    unique = {}
    for doc in documents:
        if doc["filename"] not in unique:
            unique[doc["filename"]] = doc
    return list(unique.values())

@router.delete("/document/{service_id}/{filename}")
def delete_document(service_id: str, filename: str):
    result = delete_document_by_filename(service_id, filename)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "success", "filename": filename}
