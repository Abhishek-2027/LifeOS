# backend/app/api/v1/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview")
async def overview(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await AnalyticsService.generate_dashboard(
        db,
        current_user.id
    )