# backend/app/services/memory_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.memory import Memory
from app.schemas.memory_schema import MemoryCreate
from app.memory_engine.embeddings import embed_text
import numpy as np


class MemoryService:

    @staticmethod
    async def add_memory(db: AsyncSession, user_id: int, memory_data: MemoryCreate):

        embedding = embed_text(memory_data.text)

        memory = Memory(
            user_id=user_id,
            text=memory_data.text,
            memory_type=memory_data.memory_type,
            emotion=memory_data.emotion,
            importance=memory_data.importance,
            embedding=embedding
        )

        db.add(memory)
        await db.commit()
        await db.refresh(memory)

        return memory

    @staticmethod
    async def search_memory(db: AsyncSession, user_id: int, query: str, k: int = 5):

        query_vector = embed_text(query)

        stmt = (
            select(Memory)
            .where(Memory.user_id == user_id)
            .order_by(Memory.embedding.cosine_distance(query_vector))
            .limit(k)
        )

        result = await db.execute(stmt)
        memories = result.scalars().all()

        return memories