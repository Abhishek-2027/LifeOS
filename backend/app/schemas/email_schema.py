# backend/app/schemas/email_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ----------- Create -----------

class EmailCreate(BaseModel):
    subject: Optional[str]
    sender: Optional[str]
    snippet: Optional[str]


# ----------- Response -----------

class EmailResponse(BaseModel):
    id: int
    subject: Optional[str]
    sender: Optional[str]
    snippet: Optional[str]
    is_processed: bool
    created_at: datetime

    class Config:
        from_attributes = True