from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.checkin import CheckInCreate, CheckInResponse
from app.models.checkin import CheckIn
from app.db.session import get_db

router = APIRouter(prefix="/checkin", tags=["Check-In"])

@router.post("/", response_model=CheckInResponse)
def create_checkin(checkin: CheckInCreate, db: Session = Depends(get_db)):
    new_checkin = CheckIn(**checkin.dict())
    db.add(new_checkin)
    db.commit()
    db.refresh(new_checkin)
    return new_checkin
