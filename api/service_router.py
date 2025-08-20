from fastapi import APIRouter, HTTPException

from schemas.service_schemas import ServiceCreate, ServiceResponse, ServiceUpdate
from services.company_service import (
    create_service_db,
    get_all_services_db,
    get_service_by_id_db,
    update_service_db,
    delete_service_db
)

router = APIRouter()

@router.post("/service", response_model=ServiceResponse)
def create_service(service: ServiceCreate):
    result = create_service_db(service.name, service.description)
    if result:
        return result
    raise HTTPException(status_code=400, detail="Service creation failed")


@router.get("/service", response_model=list[ServiceResponse])
def list_services():
    result = get_all_services_db()
    return result


@router.get("/service/{service_id}", response_model=ServiceResponse)
def get_service(service_id: str):
    result = get_service_by_id_db(service_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Service not found")


@router.put("/service/{service_id}", response_model=ServiceResponse)
def update_service(service_id: str, service: ServiceUpdate):
    data = service.model_dump(exclude_unset=True)
    result = update_service_db(service_id, data)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Service not found")


@router.delete("/service/{service_id}")
def delete_service(service_id: str):
    result = delete_service_db(service_id)
    if result:
        return {"message": "Service deleted"}
    raise HTTPException(status_code=404, detail="Service not found")
