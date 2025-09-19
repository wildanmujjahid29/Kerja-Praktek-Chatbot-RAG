from fastapi import APIRouter, Depends, HTTPException

from dependencies.auth_deps import admin_required
from schemas.prompt_schemas import PromptResponse, PromptUpdate
from services.prompt_service import (
    delete_prompt_db, 
    get_prompt_db,
    update_prompt_db
)

router = APIRouter()


@router.get("/chatbot/config",  response_model=PromptResponse)
def get_chatbot_config(admin=Depends(admin_required)):
    result = get_prompt_db()
    if not result:
        raise HTTPException(status_code=404, detail="Chatbot config not found")
    return result

@router.put("/chatbot/config/{config_id}", response_model=PromptResponse)
def update_chatbot_config(config_id: str, prompt: PromptUpdate, admin=Depends(admin_required)):
    data = prompt.model_dump(exclude_unset=True)
    result = update_prompt_db(config_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Failed to update chatbot config")
    return result

@router.delete("/chatbot/config/{config_id}")
def delete_chatbot_config(config_id: str, admin=Depends(admin_required)):
    result = delete_prompt_db(config_id)
    if not result:
        raise HTTPException(status_code=404, detail="Failed to delete chatbot config")
    return {"message": "Chatbot config deleted successfully"}
