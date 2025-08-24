from fastapi import APIRouter, HTTPException
from schemas.rag_schemas import RAGRequest
from services.rag_service import run_rag

router = APIRouter()

@router.post("/{service_id}")
def rag_answer(service_id: str, body: RAGRequest):
    try:
        result = run_rag(
            service_id=service_id,
            query=body.query,
            k=body.k or 4,
            min_similarity=body.min_similarity or 0.4
        )
        return {
            "status": "success",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
