from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.checkin import CheckIn
from app.schemas.checkin import CheckInCreate, CheckInResponse

router = APIRouter(prefix="/checkins", tags=["Check-Ins"])


@router.post("/", response_model=CheckInResponse)
def create_checkin(checkin: CheckInCreate, db: Session = Depends(get_db)):
    db_checkin = CheckIn(
        employee_name=checkin.employee_name,
        temperature=checkin.temperature,
        symptoms=checkin.symptoms
    )
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)
    return db_checkin


@router.get("/", response_model=list[CheckInResponse])
def get_checkins(db: Session = Depends(get_db)):
    return db.query(CheckIn).all()


@router.get("/{checkin_id}", response_model=CheckInResponse)
def get_checkin(checkin_id: int, db: Session = Depends(get_db)):
    checkin = db.query(CheckIn).filter(CheckIn.id == checkin_id).first()
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found")
    return checkin