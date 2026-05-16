from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone

from app.db.base import Base


class DataBreach(Base):
    __tablename__ = "data_breaches"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    affected_individuals = Column(Integer, nullable=False)
    data_types_affected = Column(String, nullable=False)
    reported_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reported_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ico_deadline = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(hours=72))
    ico_notified = Column(Boolean, default=False)
    ico_notified_at = Column(DateTime, nullable=True)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    severity = Column(String, default="medium")