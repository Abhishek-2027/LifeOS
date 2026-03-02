# backend/app/services/memory_service.py

import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.memory import Memory
from app.services.embedding_service import EmbeddingService


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
        
        # Try to generate embedding for the memory
        embedding = await EmbeddingService.get_embedding(memory.text)
        if embedding:
            try:
                meta = json.loads(memory.meta_data or "{}")
                meta["embedding"] = embedding
                memory.meta_data = json.dumps(meta)
                await db.commit()
            except:
                pass

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
        
        # Try semantic search first
        query_embedding = await EmbeddingService.get_embedding(query)
        memory_results = []
        
        if query_embedding:
            # Compute similarity scores
            scored = []
            for m in all_memories:
                sim = 0.0
                if m.meta_data:
                    try:
                        meta = json.loads(m.meta_data)
                        if "embedding" in meta:
                            sim = EmbeddingService.cosine_similarity(query_embedding, meta["embedding"])
                    except:
                        pass
                scored.append((m, sim))
            
            scored.sort(key=lambda x: x[1], reverse=True)
            memory_results = [
                {
                    "id": m.id,
                    "text": m.text,
                    "memory_type": m.memory_type,
                    "emotion": m.emotion,
                    "importance": m.importance,
                    "similarity_score": round(s, 2),
                    "created_at": str(m.created_at) if m.created_at else None,
                }
                for m, s in scored[:k] if s > 0.0
            ]
        
        # Fallback to text search
        if not memory_results:
            query_lower = query.lower()
            matching = [m for m in all_memories if query_lower in m.text.lower()]
            memory_results = [
                {
                    "id": m.id,
                    "text": m.text,
                    "memory_type": m.memory_type,
                    "emotion": m.emotion,
                    "importance": m.importance,
                    "similarity_score": 0.85,
                    "created_at": str(m.created_at) if m.created_at else None,
                }
                for m in matching[:k]
            ]
        
        return memory_results