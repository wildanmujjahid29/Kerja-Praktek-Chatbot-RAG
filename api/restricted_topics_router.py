from fastapi import APIRouter, HTTPException

from schemas.restricted_topics_schemas import (RestrictedTopicCreate,
                                                RestrictedTopicResponse)
from services.restricted_topics_service import (create_topic_db,
                                                delete_topic_db,
                                                get_active_topics_db,
                                                get_topics_db,
                                                toggle_all_topics_db,
                                                update_topic_db)

router = APIRouter(prefix="/topic")

@router.post("/", response_model=RestrictedTopicResponse)
def create_topic(topic: RestrictedTopicCreate):
    result = create_topic_db(topic.prompt_id, topic.topic, topic.enabled)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create topic")
    return result

@router.get("/{prompt_id}", response_model=list[RestrictedTopicResponse])
def get_topics(prompt_id: str):
    return get_topics_db(prompt_id)

@router.get("/{prompt_id}/active", response_model=list[RestrictedTopicResponse])
def get_active_topics(prompt_id: str):
    """Get only active (enabled) topics"""
    return get_active_topics_db(prompt_id)

@router.put("/{topic_id}", response_model=RestrictedTopicResponse)
def update_topic(topic_id: str, update_data: dict):
    result = update_topic_db(topic_id, update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Failed to update topic")
    return result

@router.put("/{prompt_id}/toggle-all")
def toggle_all_topics(prompt_id: str, enabled: bool):
    """Toggle all topics for a prompt on or off"""
    result = toggle_all_topics_db(prompt_id, enabled)
    return {"message": f"All topics {'enabled' if enabled else 'disabled'} successfully", "updated_count": len(result)}

@router.delete("/{topic_id}")
def delete_topic(topic_id: str):
    result = delete_topic_db(topic_id)
    if not result:
        raise HTTPException(status_code=404, detail="Failed to delete topic")
    return {"message": "Topic deleted successfully"}