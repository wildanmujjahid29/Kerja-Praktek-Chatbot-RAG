from fastapi import APIRouter, HTTPException, Depends
from schemas.config_schemas import ConfigSchema
from services.config_service import get_config_db, set_config_db
from dependencies.auth_deps import admin_required

router = APIRouter(prefix="/token")

@router.get("/")
async def get_config(admin=Depends(admin_required)):
    value = get_config_db()
    if value is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"key": "api_key", "value": value}

@router.post("/")
async def set_config(config: ConfigSchema, admin=Depends(admin_required)):
    result = set_config_db(config.value)
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to set configuration")
    return {"message": "Configuration set successfully", "data": result}