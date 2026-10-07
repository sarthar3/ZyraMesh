from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from app.core.logging import logger

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def check_db_connection() -> dict:
    """Helper for readiness probe to ping database engine"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": settings.DATABASE_URL.split(":")[0]}
    except Exception as e:
        logger.error(f"Database readiness check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
