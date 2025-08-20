from fastapi import APIRouter, HTTPException

from schemas.prompt_schemas import PromptCreate, PromptResponse, PromptUpdate
from services.prompt_service import (
    create_prompt_db,
    get_prompt_db,
    update_prompt_db,
    delete_prompt_db
)

router = APIRouter()

@router.post("/prompt", response_model=PromptResponse)
def create_prompt(service_id: str, prompt: PromptCreate):
    result = create_prompt_db(service_id, prompt.prompt)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create prompt")
    return result

@router.get("/prompt/{service_id}",  response_model=PromptResponse)
def get_prompt(service_id: str):
    result = get_prompt_db(service_id)
    if not result:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return result

@router.put("/prompt/{prompt_id}", response_model=PromptResponse)
def update_prompt(prompt_id: str, prompt: PromptUpdate):
    data = prompt.model_dump(exclude_unset=True)
    result = update_prompt_db(prompt_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Failed to update prompt")
    return result

@router.delete("/prompt/{prompt_id}")
def delete_promt(prompt_id: str):
    result = delete_prompt_db(prompt_id)
    if not result:
        raise HTTPException(status_code=404, detail="Failed to delete prompt")
    return {"message": "Prompt deleted successfully"}
