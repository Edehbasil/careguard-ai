from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base

class CheckIn(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, index=True)
    temperature = Column(Float)
    symptoms = Column(String, nullable=True)
