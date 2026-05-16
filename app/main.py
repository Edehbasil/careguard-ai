from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.routers.auth import router as auth_router
from app.routers.checkin import router as checkin_router

# Import models so Base knows about them before create_all
from app.models import checkin  # noqa
from app.db.models import user  # noqa

app = FastAPI(title="CareGuard")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(checkin_router)