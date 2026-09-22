from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models import refresh_token, user  # noqa: F401


app = FastAPI(
    title=settings.app_name,
    version="1.1.0",
    description="Authentication API for backend portfolio practice.",
)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": settings.app_name}


app.include_router(auth_router)
app.include_router(users_router)
