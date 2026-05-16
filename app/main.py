from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.routers.auth import router as auth_router
from app.routers.checkin import router as checkin_router
from app.routers.sar import router as sar_router
from app.routers.audit import router as audit_router
from app.routers.breach import router as breach_router
from app.routers.summary import router as summary_router

import app.models  # noqa

app = FastAPI(title="CareGuard")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(checkin_router)
app.include_router(sar_router)
app.include_router(audit_router)
app.include_router(breach_router)
app.include_router(summary_router)