import os
import shutil
import uuid

from fastapi import APIRouter, Form, HTTPException, UploadFile, Depends

from schemas.document_schemas import (DocumentOut, DocumentTagOut,
                                      UniqueTagsResponse, UpdateTagRequest)
from services.document_service import (delete_document_by_filename,
                                       delete_document_by_id,
                                       get_all_documents,
                                       get_documents_by_service_tag,
                                       get_unique_service_tags,
                                       remove_tag_from_document_by_filename,
                                       update_document_tag_by_filename)
from services.embed_service import embedding_text_from_file
from dependencies.auth_deps import admin_required

router = APIRouter()


@router.post("/document/embed")
async def embed_file(file: UploadFile = None, service_tag: str = Form(None), admin=Depends(admin_required)):
    # simpan file sementara
    temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # proses embedding dengan metadata
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
def list_all_documents(admin=Depends(admin_required)):
    documents = get_all_documents()
    unique = {}
    for doc in documents:
        if doc["filename"] not in unique:
            unique[doc["filename"]] = doc
    return list(unique.values())

@router.get("/document/service/{service_tag}", response_model=list[DocumentOut])
def list_documents_by_service_tag(service_tag: str, admin=Depends(admin_required)):
    if service_tag.lower() in ["null", "none", "empty"]:
        service_tag = None
        
    documents = get_documents_by_service_tag(service_tag)
    # Filter unik berdasarkan filename
    unique = {}
    for doc in documents:
        if doc["filename"] not in unique:
            unique[doc["filename"]] = doc
    return list(unique.values())

@router.delete("/document/filename/{filename}")
def delete_document_by_name(filename: str, admin=Depends(admin_required)):
    result = delete_document_by_filename(filename)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "success", "filename": filename}

@router.delete("/document/id/{document_id}", include_in_schema=False)
def delete_document_by_document_id(document_id: str, admin=Depends(admin_required)):
    result = delete_document_by_id(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "success", "document_id": document_id}

@router.put("/document/filename/{filename}/tag")
def update_tag_by_filename(filename: str, request: UpdateTagRequest, admin=Depends(admin_required)):
    result = update_document_tag_by_filename(filename, request.service_tag)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "success", "filename": filename, "new_tag": request.service_tag}

@router.delete("/document/filename/{filename}/tag")
def remove_tag_by_filename(filename: str, admin=Depends(admin_required)):
    result = remove_tag_from_document_by_filename(filename)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "success", "filename": filename, "message": "Tag removed"}

@router.get("/document/tags", response_model=UniqueTagsResponse)
def get_unique_document_tags(admin=Depends(admin_required)):
    tags = get_unique_service_tags()
    return UniqueTagsResponse(tags=tags)
