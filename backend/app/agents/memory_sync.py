# backend/app/agents/memory_sync.py

from app.services.memory_service import MemoryService
from app.schemas.memory_schema import MemoryCreate

class MemorySync:

    async def sync(self, db, user_id, output: str):

        memory_data = MemoryCreate(
            text=output,
            memory_type="agent_generated",
            emotion=None,
            importance=0.7
        )

        await MemoryService.add_memory(db, user_id, memory_data)