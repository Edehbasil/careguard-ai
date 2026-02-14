from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.checkin import HealthCheckCreate
from app.models.checkin import CheckIn
from app.routers import checkin

app = FastAPI()

app.include_router(checkin.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/health-checks/", response_model=dict)
def create_health_check(check: HealthCheckCreate, db: Session = Depends(get_db)):
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
