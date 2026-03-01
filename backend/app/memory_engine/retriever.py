# backend/app/memory_engine/retriever.py

from app.services.memory_service import MemoryService

class MemoryRetriever:

    async def retrieve(self, db, user_id, query, k=5):
        return await MemoryService.search_memory(db, user_id, query, k)