import os
import shutil
import uuid

from fastapi import APIRouter, Form, HTTPException, UploadFile

from schemas.document_schemas import DocumentOut
from services.document_service import (delete_document_by_filename,
                                       delete_document_by_id,
                                       get_all_documents,
                                       get_documents_by_service_tag)
from services.embed_service import embedding_text_from_file

router = APIRouter()


@router.post("/document/embed")
async def embed_file(file: UploadFile = None, service_tag: str = Form(None)):
    # simpan file sementara
    temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # proses embedding dengan metadata (service_tag optional for admin categorization)
    result = embedding_text_from_file(temp_filename, file.filename, service_tag)

    # hapus file sementara
    os.remove(temp_filename)
    return {
        "status": "success",
        "filename": file.filename,
        "file_type": file.filename.split(".")[-1].lower(),
        "chunks_saved": len(result)
    }

@router.get("/document", response_model=list[DocumentOut])
def list_all_documents():
    documents = get_all_documents()
    # Filter unik berdasarkan filename
    unique = {}
    for doc in documents:
        if doc["filename"] not in unique:
            unique[doc["filename"]] = doc
    return list(unique.values())

@router.get("/document/service/{service_tag}", response_model=list[DocumentOut])  
def list_documents_by_service_tag(service_tag: str):
    documents = get_documents_by_service_tag(service_tag)
    # Filter unik berdasarkan filename
    unique = {}
    for doc in documents:
        if doc["filename"] not in unique:
            unique[doc["filename"]] = doc
    return list(unique.values())

@router.delete("/document/filename/{filename}")
def delete_document_by_name(filename: str):
    result = delete_document_by_filename(filename)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "success", "filename": filename}

@router.delete("/document/id/{document_id}")
def delete_document_by_document_id(document_id: str):
    result = delete_document_by_id(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "success", "document_id": document_id}
