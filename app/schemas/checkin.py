##from pydantic import BaseModel
##from typing import Optional

##class HealthCheckCreate(BaseModel):
  ##  employee_name: str
    ##temperature: str
    ##symptoms: Optional[str] = None

    ##model_config = {
     ##   "from_attributes": True
    ##}
from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter

router = APIRouter()

@router.post("/checkin")
def create_checkin():
    return {"message": "Check-in created"}

class HealthCheckCreate(BaseModel):
    employee_name: str
    temperature: str
    symptoms: Optional[str] = None

class CheckInCreate(BaseModel):
    employee_name: str
    temperature: str
    symptoms: Optional[str] = None

class CheckInResponse(BaseModel):
    id: int
    employee_name: str
    temperature: str
    symptoms: Optional[str]

    class Config:
        orm_mode = True

