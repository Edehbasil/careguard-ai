from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
import enum

from app.db.base import Base


class SARStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    closed = "closed"


class SubjectAccessRequest(Base):
    __tablename__ = "subject_access_requests"

    id = Column(Integer, primary_key=True, index=True)
    requester_name = Column(String, nullable=False)
    requester_email = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default=SARStatus.pending)
    submitted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    deadline = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=30))
    resolved_at = Column(DateTime, nullable=True)
    submitted_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    submitted_by = relationship("User", back_populates="sar_requests")