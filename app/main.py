from fastapi import FastAPI, Depends
from app.routers.auth import router as auth_router
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.checkin import CheckInCreate, CheckInResponse
from app.models.checkin import CheckIn
from app.routers import checkin
from fastapi import HTTPException
from app.models.checkin import CheckIn
from app.db.session import get_db
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.database import engine, Base
from app.models import user
import os



app = FastAPI()
Base.metadata.create_all(bind=engine)
print(os.listdir("app/db"))
app.include_router(checkin.router)
app.include_router(auth_router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/health-checks/", response_model=dict)
def create_health_check(check: CheckInCreate, db: Session = Depends(get_db)):
    """
    Create a new health check record in the database.
    """
    db_check = CheckIn(
        employee_name=check.employee_name,
        temperature=check.temperature,
        symptoms=check.symptoms
    )

    db.add(db_check)
    db.commit()
    db.refresh(db_check)

    return {"message": "Health check submitted successfully", "id": db_check.id}

@app.get("/checkins", response_model=list[CheckInResponse])
def get_checkins():
    db = SessionLocal()
    checkins = db.query(CheckIn).all()
    db.close()
    return checkins

@app.get("/checkins/{checkin_id}", response_model=CheckInResponse)
def get_checkin(checkin_id: int):
    db = SessionLocal()
    checkin = db.query(CheckIn).filter(CheckIn.id == checkin_id).first()
    db.close()

    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found")

    return checkin

@app.get("/checkins", response_model=list[CheckInResponse])
def read_checkins(db: Session = Depends(get_db)):
    return db.query(CheckIn).all()