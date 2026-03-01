# backend/app/memory_engine/memory_manager.py

from app.memory_engine.embeddings import embed_text
from app.memory_engine.importance import ImportanceScorer
from app.services.memory_service import MemoryService
from app.schemas.memory_schema import MemoryCreate


class MemoryManager:

    def classify(self, structured_memory):

        if structured_memory.get("events"):
            return "episodic"

        if structured_memory.get("topics"):
            return "semantic"

        return "episodic"

    async def add(self, db, user_id, structured_memory):

        memory_type = self.classify(structured_memory)

        memory_data = MemoryCreate(
            text=structured_memory["raw_text"],
            memory_type=memory_type,
            emotion=structured_memory.get("emotion"),
            importance=self.importance.score(structured_memory)
        )

        return await MemoryService.add_memory(db, user_id, memory_data)