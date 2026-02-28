# backend/app/schemas/memory_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ----------- Create -----------

class MemoryCreate(BaseModel):
    text: str
    memory_type: str  # episodic / semantic / document / email
    emotion: Optional[str] = None
    importance: Optional[float] = 0.5


# ----------- Response -----------

class MemoryResponse(BaseModel):
    id: int
    text: str
    memory_type: str
    emotion: Optional[str]
    importance: float
    created_at: datetime

    class Config:
        from_attributes = True


# ----------- Search Response -----------

class MemorySearchResult(BaseModel):
    id: int
    text: str
    similarity_score: float