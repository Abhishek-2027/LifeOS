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

    @staticmethod
    async def generate_dashboard(db: AsyncSession, user_id: int):
        count = await AnalyticsService.memory_count(db, user_id)
        dist = await AnalyticsService.emotion_distribution(db, user_id)
        return {
            "memory_count": count,
            "emotion_distribution": [{"emotion": e[0], "count": e[1]} for e in dist] if dist else [],
            "message": "Dashboard overview"
        }
