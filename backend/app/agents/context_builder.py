# backend/app/agents/context_builder.py

from app.services.memory_service import MemoryService

class ContextBuilder:

    def __init__(self, db, user_id):
        self.db = db
        self.user_id = user_id

    async def build(self, query: str):

        memories = await MemoryService.search_memory(
            self.db,
            self.user_id,
            query,
            k=5
        )

        context = "\n".join(
            [f"- {m.text} (importance: {m.importance})" for m in memories]
        )

        return context