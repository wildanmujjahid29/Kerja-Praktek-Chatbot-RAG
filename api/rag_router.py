from fastapi import APIRouter, Depends, HTTPException

from dependencies.auth_deps import admin_required
from schemas.rag_schemas import RAGRequest, RAGResponse
from services.rag_service import run_rag

router = APIRouter()

# Testing Pesan
@router.post("/rag", response_model=RAGResponse)
def rag_answer(body: RAGRequest, _: object = Depends(admin_required)):
    try:
        result = run_rag(
            query=body.query,
            k=body.k,
            min_similarity=body.min_similarity,
        )
        return result
    except Exception as e:
        # Re-raise with context to preserve traceback in logs
        raise HTTPException(status_code=500, detail=str(e)) from e
