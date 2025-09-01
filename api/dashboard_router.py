from fastapi import APIRouter, HTTPException, Query
from typing import List

from services.dashboard_service import get_overview_stats_db, get_service_stats_db
from schemas.dashboard_schemas import OverviewStats, ServiceStats

router = APIRouter(prefix="/dashboard")

@router.get("/overview")
def get_overview() -> OverviewStats:
    try:
        stats = get_overview_stats_db()
        return OverviewStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/services-stats")
def get_services_stats() -> List[ServiceStats]:
    try:
        stats = get_service_stats_db()
        return [ServiceStats(**stat) for stat in stats]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))