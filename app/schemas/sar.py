from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.sar import SARStatus


class SARCreate(BaseModel):
    requester_name: str
    requester_email: EmailStr
    description: str


class SARStatusUpdate(BaseModel):
    status: SARStatus


class SARResponse(BaseModel):
    id: int
    requester_name: str
    requester_email: str
    description: str
    status: SARStatus
    submitted_at: datetime
    deadline: datetime
    resolved_at: Optional[datetime] = None
    submitted_by_user_id: Optional[int] = None
    days_remaining: Optional[int] = None

    model_config = {"from_attributes": True}