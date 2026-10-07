from fastapi import APIRouter, Depends, status, Response
from pydantic import BaseModel
from typing import Dict, Any
from app.core.config import settings
from app.core.database import check_db_connection
from app.core.redis import redis_manager

router = APIRouter(tags=["Health & Infrastructure"])

class HealthCheckResponse(BaseModel):
    status: str
    version: str
    environment: str

class ReadinessCheckResponse(BaseModel):
    status: str
    database: Dict[str, Any]
    redis: Dict[str, Any]

@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    """Liveness probe to confirm backend API is alive"""
    return HealthCheckResponse(
        status="ok",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT
    )

@router.get("/ready", response_model=ReadinessCheckResponse)
def readiness_check(response: Response):
    """Readiness probe to confirm Database and Redis connectivity"""
    db_status = check_db_connection()
    redis_status = redis_manager.check_connection()

    is_healthy = (db_status.get("status") == "healthy") and (redis_status.get("status") == "healthy")
    if not is_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return ReadinessCheckResponse(
        status="ready" if is_healthy else "unhealthy",
        database=db_status,
        redis=redis_status
    )
