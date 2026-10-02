import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.logging import configure_logging


configure_logging()

logger = logging.getLogger(__name__)

settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for Best Hospital Salem AI Platform",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health_router,
    prefix="/api/v1",
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Best Hospital Salem AI API",
        "docs": "/docs",
    }


@app.on_event("startup")
def startup_event() -> None:
    logger.info(
        "%s version %s starting",
        settings.app_name,
        settings.app_version,
    )