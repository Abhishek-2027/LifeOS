# backend/app/api/v1/memory.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.memory_service import MemoryService
from app.schemas.memory_schema import MemoryCreate

router = APIRouter(prefix="/memory", tags=["Memory"])


@router.post("/add")
async def add_memory(
    memory: MemoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await MemoryService.add_memory(
        db,
        current_user.id,
        memory
    )


@router.get("/search")
async def search_memory(
    query: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await MemoryService.search(
        db,
        current_user.id,
        query
    )