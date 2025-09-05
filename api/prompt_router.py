from fastapi import APIRouter, HTTPException

from schemas.prompt_schemas import PromptCreate, PromptResponse, PromptUpdate
from services.prompt_service import (create_prompt_db, delete_prompt_db,
                                     get_prompt_db, update_prompt_db)

router = APIRouter()

@router.post("/chatbot/config", response_model=PromptResponse)
def create_chatbot_config(prompt: PromptCreate):
    result = create_prompt_db(prompt.prompt, prompt.fallback_response)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create chatbot config")
    return result

@router.get("/chatbot/config",  response_model=PromptResponse)
def get_chatbot_config():
    result = get_prompt_db()
    if not result:
        raise HTTPException(status_code=404, detail="Chatbot config not found")
    return result

@router.put("/chatbot/config/{config_id}", response_model=PromptResponse)
def update_chatbot_config(config_id: str, prompt: PromptUpdate):
    data = prompt.model_dump(exclude_unset=True)
    result = update_prompt_db(config_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Failed to update chatbot config")
    return result

@router.delete("/chatbot/config/{config_id}")
def delete_chatbot_config(config_id: str):
    result = delete_prompt_db(config_id)
    if not result:
        raise HTTPException(status_code=404, detail="Failed to delete chatbot config")
    return {"message": "Chatbot config deleted successfully"}
