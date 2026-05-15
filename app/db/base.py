from sqlalchemy.orm import declarative_base
from app.db.session import engine
from app.models.checkin import CheckIn

Base = declarative_base()
CheckIn.metadata.create_all(bind=engine)
