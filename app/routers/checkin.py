from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.checkin import CheckIn
from app.schemas.checkin import CheckInCreate, CheckInResponse

router = APIRouter()

@router.post("/checkins", response_model=CheckInResponse)
def create_checkin(checkin: CheckInCreate, db: Session = Depends(get_db)):
    db_checkin = CheckIn(**checkin.dict())
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)
    return db_checkin

@router.get("/checkins")
def get_checkins(db: Session = Depends(get_db)):
    return db.query(CheckIn).all()
