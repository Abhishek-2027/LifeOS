from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.reasoning_service import ReasoningService

router = APIRouter(prefix="/reasoning", tags=["Reasoning"])


@router.get("/analyze")
async def analyze(
    query: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await ReasoningService.reason(
        db=db,
        user_id=current_user.id,
        query=query
    )