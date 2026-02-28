# backend/app/models/agent_log.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class AgentLog(Base, TimestampMixin):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    agent_name = Column(String(100))
    action = Column(String(255))
    details = Column(Text)

    user = relationship("User", back_populates="agent_logs")