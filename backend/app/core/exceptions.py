from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logging import logger

class ZyraException(Exception):
    """Base exception for Zyra Platform"""
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class MarketplaceException(ZyraException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST, details=details)

class OrchestrationException(ZyraException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, details=details)

class TrustException(ZyraException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST, details=details)

async def zyra_exception_handler(request: Request, exc: ZyraException):
    logger.error(f"ZyraException caught: {exc.message} | Path: {request.url.path} | Details: {exc.details}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "details": exc.details,
            "path": str(request.url.path)
        }
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception caught on path {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "An unexpected internal server error occurred",
            "path": str(request.url.path)
        }
    )
