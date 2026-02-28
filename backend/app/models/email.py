# backend/app/models/email.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Email(Base, TimestampMixin):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    subject = Column(String(255))
    sender = Column(String(255))
    snippet = Column(Text)
    is_processed = Column(Boolean, default=False)

    user = relationship("User", back_populates="emails")