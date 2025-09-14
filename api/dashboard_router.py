from fastapi import APIRouter, Depends, HTTPException

from dependencies.auth_deps import admin_required
from schemas.dashboard_schemas import (MonthlyAnalyticsItem,
                                       MonthlyAnalyticsResponse, OverviewStats)
from services.dashboard_service import (get_monthly_analytics_db,
                                        get_monthly_daily_sessions_db,
                                        get_overview_stats_db)

router = APIRouter(prefix="/dashboard")

@router.get("/overview")
def get_overview(admin=Depends(admin_required)) -> OverviewStats:
    try:
        stats = get_overview_stats_db()
        return OverviewStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monthly-analytics")
def get_monthly_analytics(admin=Depends(admin_required)) -> MonthlyAnalyticsResponse:
    try:
        result = get_monthly_analytics_db()
        return MonthlyAnalyticsResponse(items=[MonthlyAnalyticsItem(**item) for item in result])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monthly-daily-sessions")
def get_monthly_daily_sessions(month: str, admin=Depends(admin_required)):
    try:
        result = get_monthly_daily_sessions_db(month)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
