from fastapi import APIRouter, HTTPException
from services.retrieval_service import search_similar_documents, get_context_from_results

router = APIRouter()

@router.post("/retrieval/{service_id}")
def test_retrieval(service_id: str, query: str, match_threshold: float = 0.7, match_count: int = 5):
    try:
        # Call retrieval service
        search_results = search_similar_documents(service_id, query, match_threshold, match_count)
        # Format search results into context
        context = get_context_from_results(search_results)
        return {
            "status": "success",
            "query": query,
            "context": context
        }
    except HTTPException as e:
        return {"status": "error", "detail": str(e)}