from typing import List

from fastapi import APIRouter, HTTPException, Query

from schemas.dashboard_schemas import (MonthlyAnalyticsItem,
                                       MonthlyAnalyticsResponse, OverviewStats,
                                       ServiceStats)
from services.dashboard_service import (get_monthly_analytics_db,
                                        get_overview_stats_db,
                                        get_service_stats_db,
                                        get_monthly_daily_sessions_db)

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
    

@router.get("/monthly-analytics")
def get_monthly_analytics() -> MonthlyAnalyticsResponse:
    try:
        result = get_monthly_analytics_db()
        return MonthlyAnalyticsResponse(items=[MonthlyAnalyticsItem(**item) for item in result])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/monthly-daily-sessions")
def get_monthly_daily_sessions(month: str):
    try:
        result = get_monthly_daily_sessions_db(month)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))