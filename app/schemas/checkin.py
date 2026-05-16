from pydantic import BaseModel, Field
from typing import Optional


class CheckInCreate(BaseModel):
    employee_name: str
    temperature: float = Field(..., ge=34.0, le=42.0)
    symptoms: Optional[str] = None


class CheckInResponse(BaseModel):
    id: int
    employee_name: str
    temperature: float
    symptoms: Optional[str] = None

    model_config = {"from_attributes": True}