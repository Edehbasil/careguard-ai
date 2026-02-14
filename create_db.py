import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from db.session import Base, engine
from app.models.checkin import CheckIn 

Base.metadata.create_all(bind=engine)

print("Database created successfully")
