# backend/app/services/reasoning_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.services.memory_service import MemoryService
from app.reasoning_engine.reasoning_manager import ReasoningManager


class ReasoningService:

    @staticmethod
    async def analyze(db: AsyncSession, user_id: int, query: str):

        memories = await MemoryService.search_memory(db, user_id, query)

        reasoning_manager = ReasoningManager()
        result = reasoning_manager.run_reasoning(query, memories)

        return result