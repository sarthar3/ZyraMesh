from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.core.exceptions import ZyraException, zyra_exception_handler, unhandled_exception_handler
from app.database import engine, Base, SessionLocal
from app.api.v1.router import api_v1_router
from app.services.marketplace import seed_marketplace

# Setup Structured Logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Zyra Mesh - Trust-Calibrated Dual-Graph Agent Team Formation with Uncertainty-Gated Re-Orchestration"
)

# Custom Exception Handlers
app.add_exception_handler(ZyraException, zyra_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    logger.info("Starting up Zyra Mesh backend service...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_marketplace(db)
    finally:
        db.close()

# Mount API v1 router
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

# Root Health Redirect Shortcuts
@app.get("/health", tags=["Health & Infrastructure"])
def root_health():
    return {"status": "ok", "version": settings.VERSION}

@app.get("/")
def root_status():
    return {
        "status": "ONLINE",
        "system": settings.PROJECT_NAME,
        "docs": "/docs",
        "version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
