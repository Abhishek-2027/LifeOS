# backend/app/schemas/document_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ----------- Create -----------

class DocumentCreate(BaseModel):
    filename: str
    content_summary: Optional[str] = None


# ----------- Response -----------

class DocumentResponse(BaseModel):
    id: int
    filename: str
    content_summary: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True