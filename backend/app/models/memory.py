from sqlalchemy import Column, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import func
import uuid

from app.models.base import Base


class Memory(Base):
    __tablename__ = "memories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    text = Column(Text, nullable=False)
    memory_type = Column(String, nullable=False)

    embedding = Column(Vector(384))  # IMPORTANT

    emotion = Column(String)
    importance = Column(Float, default=0.5)

    meta_data = Column(JSONB)

    created_at = Column(DateTime(timezone=True), server_default=func.now())