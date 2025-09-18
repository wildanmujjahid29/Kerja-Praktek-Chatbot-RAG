import os
import shutil
import uuid

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile

from dependencies.auth_deps import admin_required
from schemas.document_schemas import (DocumentOut,
                                    KnowledgeInput, 
                                    UniqueTagsResponse,
                                    UpdateTagRequest,
                                    DocumentChunkUpdateRequest,
                                    DocumentChunkUpdateResponse,
                                    ChunkBatchUpdateRequest,
                                    ChunkBatchUpdateResponse)
from services.document_service import (delete_document_by_filename,
                                    delete_document_by_id,
                                    get_all_documents,
                                    get_documents_by_service_tag,
                                    get_unique_service_tags,
                                    remove_tag_from_document_by_filename,
                                    update_document_tag_by_filename,
                                    get_document_chunk_by_id,
                                    update_document_chunk,
                                    update_document_chunks_batch)
from services.embed_service import (chunk_text, embedding_text_from_file,
                                    embedding_text_from_input,
                                    load_text_from_file, preprocess_text)

router = APIRouter()

@router.post("/document/test-chunk")
async def test_chunk(file: UploadFile = None, admin=Depends(admin_required)):
    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded")
    # simpan file sementara
    temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)   
    
    # load & preprocess
    text = load_text_from_file(temp_filename)
    text = preprocess_text(text)

    # chunk pakai Chonkie
    chunks = chunk_text(text)
    
    # hapus file sementara
    os.remove(temp_filename)

    # return chunk hasil (tanpa embed)
    return {
        "status": "success",
        "filename": file.filename,
        "chunk_details": [
            {"index": i + 1, "text": chunk, "length": len(chunk)} for i, chunk in enumerate(chunks)
        ],
        "total_chunks": len(chunks)
    }
    

@router.post("/document/embed-document")
async def embed_file(file: UploadFile = None, service_tag: str = Form(None), admin=Depends(admin_required)):
    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded")
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
        "service_tag": service_tag,
        # list of raw chunk texts for convenience
        "chunks": [row["content"] for row in result],
        # detailed metadata per chunk
        "chunk_details": [
            {"index": i + 1, "text": row["content"], "length": len(row["content"])} for i, row in enumerate(result)
        ],
        "chunks_saved": len(result)
    }

@router.post("/document/embed-text")
async def embed_text(body: KnowledgeInput, admin=Depends(admin_required)):
    virtual_filename = None
    if body.title:
        safe_title = body.title.strip().lower().replace(' ', '_')
        virtual_filename = f"{safe_title}.txt"
    result = embedding_text_from_input(body.content, virtual_filename=virtual_filename, service_tag=body.service_tag)
    return {
        "status": "success",
        "filename": virtual_filename or "manual-input.txt",
        "file_type": "txt",
        "service_tag": body.service_tag,
        "chunks": [row["content"] for row in result],
        "chunk_details": [
            {"index": i + 1, "text": row["content"], "length": len(row["content"])} for i, row in enumerate(result)
        ],
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

@router.put("/document/chunk/{document_id}", response_model=DocumentChunkUpdateResponse)
def update_chunk(document_id: str, body: DocumentChunkUpdateRequest, admin=Depends(admin_required)):
    if not body.content or not body.content.strip():
        raise HTTPException(status_code=400, detail="Content tidak boleh kosong")

    updated = update_document_chunk(document_id, body.content, body.service_tag)
    if not updated:
        raise HTTPException(status_code=404, detail="Chunk / Document ID tidak ditemukan")
    return updated

@router.put("/document/chunks/batch", response_model=ChunkBatchUpdateResponse)
def update_chunks_batch(body: ChunkBatchUpdateRequest, admin=Depends(admin_required)):
    if not body.items or len(body.items) == 0:
        raise HTTPException(status_code=400, detail="List items kosong")

    for item in body.items:
        if not item.content or not item.content.strip():
            raise HTTPException(status_code=400, detail=f"Content kosong untuk id: {item.id}")

    updated_list = update_document_chunks_batch(
        [ {"id": item.id, "content": item.content, "service_tag": item.service_tag} for item in body.items ]
    )
    return {
        "updated": updated_list,
        "total_updated": len(updated_list)
    }