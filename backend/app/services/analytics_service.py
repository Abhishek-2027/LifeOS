# backend/app/services/analytics_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.models.memory import Memory


class AnalyticsService:

    @staticmethod
    async def memory_count(db: AsyncSession, user_id: int):

        result = await db.execute(
            select(func.count(Memory.id))
            .where(Memory.user_id == user_id)
        )

        return result.scalar()

    @staticmethod
    async def emotion_distribution(db: AsyncSession, user_id: int):

        result = await db.execute(
            select(Memory.emotion, func.count())
            .where(Memory.user_id == user_id)
            .group_by(Memory.emotion)
        )

        return result.all()