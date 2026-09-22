import logging

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.core.config import settings
from app.core.errors import unhandled_exception_handler
from app.core.middleware import request_context_middleware
from app.db.base import Base
from app.db.session import engine
from app.models import refresh_token, user  # noqa: F401


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(
    title=settings.app_name,
    version="1.2.0",
    description="Authentication API for backend portfolio practice.",
)

app.middleware("http")(request_context_middleware)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.on_event("startup")
def create_tables():
    if settings.environment == "test":
        Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }


app.include_router(auth_router)
app.include_router(users_router)
