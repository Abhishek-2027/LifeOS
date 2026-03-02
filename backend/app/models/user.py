# backend/app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships - using lazy='select' for async compatibility
    memories = relationship(
        "Memory",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="Memory.user_id"
    )
    documents = relationship(
        "Document",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="Document.user_id"
    )
    emails = relationship(
        "Email",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="Email.user_id"
    )
    agent_logs = relationship(
        "AgentLog",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="AgentLog.user_id"
    )