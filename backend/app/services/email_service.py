# backend/app/services/email_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.email import Email
from app.schemas.email_schema import EmailCreate


class EmailService:

    @staticmethod
    async def add_email(db: AsyncSession, user_id: int, data: EmailCreate):

        email = Email(
            user_id=user_id,
            subject=data.subject,
            sender=data.sender,
            snippet=data.snippet
        )

        db.add(email)
        await db.commit()
        await db.refresh(email)

        return email

    @staticmethod
    async def get_unprocessed(db: AsyncSession, user_id: int):

        result = await db.execute(
            select(Email)
            .where(Email.user_id == user_id, Email.is_processed == False)
        )

        return result.scalars().all()

    @staticmethod
    async def sync_user_emails(db: AsyncSession, user_id: int):
        # placeholder: real implementation would connect to email provider
        return {"synced": 0, "message": "Email sync not yet implemented"}

    @staticmethod
    async def get_user_emails(db: AsyncSession, user_id: int):
        try:
            result = await db.execute(select(Email).where(Email.user_id == user_id))
            emails = result.scalars().all()
            return [{"id": e.id, "subject": e.subject, "sender": e.sender, "snippet": e.snippet} for e in emails]
        except Exception as e:
            # Return empty list on error instead of crashing
            return []
