# backend/app/api/v1/emails.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.email_service import EmailService

router = APIRouter(prefix="/emails", tags=["Emails"])


@router.post("/sync")
async def sync_emails(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await EmailService.sync_user_emails(
        db,
        current_user.id
    )


@router.get("/")
async def list_emails(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await EmailService.get_user_emails(
        db,
        current_user.id
    )