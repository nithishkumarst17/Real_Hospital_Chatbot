from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.db.database import check_database_connection


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

settings = get_settings()


@router.get("")
def health_check() -> dict[str, str]:
    database_healthy = check_database_connection()

    if not database_healthy:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        )

    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
        "database": "connected",
    }