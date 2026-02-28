# backend/app/models/memory.py

from sqlalchemy import Column, Integer, Text, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.models.base import Base, TimestampMixin


class Memory(Base, TimestampMixin):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    text = Column(Text, nullable=False)
    memory_type = Column(String(50), nullable=False)  # episodic / semantic / document / email

    embedding = Column(Vector(768))  # adjust dimension to your model

    emotion = Column(String(100))
    importance = Column(Float, default=0.5)

    user = relationship("User", back_populates="memories")