# backend/app/services/memory_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.models.memory import Memory
from app.memory_engine.embeddings import embed_text


class MemoryService:

    # -----------------------------
    # Store Memory
    # -----------------------------
    @staticmethod
    async def add_memory(db: AsyncSession, user_id, memory_data):

        embedding = embed_text(memory_data.text)

        memory = Memory(
            user_id=user_id,
            text=memory_data.text,
            memory_type=memory_data.memory_type,
            emotion=memory_data.emotion,
            importance=memory_data.importance,
            embedding=embedding,
        )

        db.add(memory)
        await db.commit()
        await db.refresh(memory)

        return memory

    # -----------------------------
    # Vector Similarity Search
    # -----------------------------
    @staticmethod
    async def search_memory(db: AsyncSession, user_id, query: str, k: int = 5):

        query_embedding = embed_text(query)

        stmt = text("""
            SELECT *,
            embedding <=> :embedding AS distance
            FROM memories
            WHERE user_id = :user_id
            ORDER BY embedding <=> :embedding
            LIMIT :k
        """)

        result = await db.execute(
            stmt,
            {
                "embedding": query_embedding,
                "user_id": str(user_id),
                "k": k,
            },
        )

        return result.fetchall()