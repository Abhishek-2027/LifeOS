from sqlalchemy import Column, String, Float, Text, ForeignKey, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    text = Column(Text, nullable=False)
    memory_type = Column(String, nullable=False)

    emotion = Column(String)
    importance = Column(Float, default=0.5)
    meta_data = Column(Text)  # Store JSON as text for SQLite

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="memories")