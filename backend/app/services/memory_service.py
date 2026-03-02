# backend/app/services/memory_service.py

import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.memory import Memory


class MemoryService:

    # Store Memory
    @staticmethod
    async def add_memory(db: AsyncSession, user_id, memory_data):
        """Add a new memory for the user (SQLite compatible)"""
        
        # Convert metadata to JSON string if it's a dict
        meta_data_str = None
        if hasattr(memory_data, 'dict'):
            meta_data_str = json.dumps(memory_data.dict())
        elif isinstance(memory_data, dict):
            meta_data_str = json.dumps(memory_data)
        
        memory = Memory(
            user_id=user_id,
            text=memory_data.text,
            memory_type=memory_data.memory_type,
            emotion=memory_data.emotion,
            importance=memory_data.importance,
            meta_data=meta_data_str,
        )

        db.add(memory)
        await db.commit()
        await db.refresh(memory)

        return {
            "id": memory.id,
            "text": memory.text,
            "memory_type": memory.memory_type,
            "emotion": memory.emotion,
            "importance": memory.importance,
            "created_at": str(memory.created_at) if memory.created_at else None,
        }

    # Search Memory (text-based for SQLite compatibility)
    @staticmethod
    async def search_memory(db: AsyncSession, user_id, query: str, k: int = 5):
        """Search memories using text matching (SQLite compatible)"""
        
        # Simple text search - find memories that contain the query terms
        query_lower = query.lower()
        
        stmt = select(Memory).where(
            Memory.user_id == user_id
        ).order_by(
            Memory.created_at.desc()
        )

        result = await db.execute(stmt)
        all_memories = result.scalars().all()
        
        # Filter by text content match
        matching_memories = [
            m for m in all_memories 
            if query_lower in m.text.lower()
        ]
        
        # Return top k matches
        return [
            {
                "id": m.id,
                "text": m.text,
                "memory_type": m.memory_type,
                "emotion": m.emotion,
                "importance": m.importance,
                "similarity_score": 0.9,  # Dummy score for text match
                "created_at": str(m.created_at) if m.created_at else None,
            }
            for m in matching_memories[:k]
        ]