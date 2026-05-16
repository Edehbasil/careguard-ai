from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BreachCreate(BaseModel):
    title: str
    description: str
    affected_individuals: int
    data_types_affected: str
    severity: str = "medium"


class BreachICOUpdate(BaseModel):
    ico_notified: bool


class BreachResolveUpdate(BaseModel):
    resolved: bool


class BreachResponse(BaseModel):
    id: int
    title: str
    description: str
    affected_individuals: int
    data_types_affected: str
    severity: str
    reported_by_user_id: Optional[int] = None
    reported_at: datetime
    ico_deadline: datetime
    ico_notified: bool
    ico_notified_at: Optional[datetime] = None
    resolved: bool
    resolved_at: Optional[datetime] = None
    hours_remaining: Optional[int] = None

    model_config = {"from_attributes": True}