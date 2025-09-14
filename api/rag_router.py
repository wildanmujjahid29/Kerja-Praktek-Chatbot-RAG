from fastapi import APIRouter, HTTPException, Depends

from schemas.rag_schemas import RAGRequest, RAGResponse
from services.rag_service import run_rag
from dependencies.auth_deps import admin_required
router = APIRouter()

@router.post("/rag", response_model=RAGResponse)
def rag_answer(body: RAGRequest, admin=Depends(admin_required)):
    try:
        result = run_rag(
            query=body.query,
            k=5,
            min_similarity=0.3
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
