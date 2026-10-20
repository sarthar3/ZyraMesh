import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    PROJECT_NAME: str = "Zyra Mesh - Intelligent Multi-Agent Marketplace"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development" # "development", "staging", "production"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./zyra_mesh.db"
    
    # Redis Cache / Broker (Optional)
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"
    USE_REDIS_FALLBACK: bool = True
    
    # AI Backend Providers
    DEFAULT_LLM_PROVIDER: str = "mock" # "ollama", "gemini", "mock"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_DEFAULT_MODEL: str = "qwen2.5:1.5b-instruct"
    GEMINI_API_KEY: str = ""
    GEMINI_DEFAULT_MODEL: str = "gemini-1.5-flash"
    
    # NVIDIA NIM Provider
    NVIDIA_API_KEY: str = ""
    NVIDIA_DEFAULT_MODEL: str = "meta/llama-3.1-70b-instruct"
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    
    # Speechmatics Voice-to-Text
    SPEECHMATICS_API_KEY: str = ""
    
    # Testmail Notifications & Audit
    TESTMAIL_API_KEY: str = ""
    TESTMAIL_NAMESPACE: str = "u5api"
    
    # Security & CORS

    SECRET_KEY: str = "zyra-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"]
    
    # Execution & Trust Engine Settings
    DEFAULT_TRUST_MEAN: float = 0.5
    DEFAULT_TRUST_UNCERTAINTY: float = 0.5
    UNCERTAINTY_VERIFICATION_THRESHOLD: float = 0.40
    FAILURE_PROPAGATION_THRESHOLD: float = 0.60

settings = Settings()
