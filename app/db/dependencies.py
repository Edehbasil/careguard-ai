# app/db/dependencies.py
from app.db.database import SessionLocal
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db():
    """
    Async-compatible DB session dependency for FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()