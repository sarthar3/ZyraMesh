import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Zyra Mesh - Intelligent Multi-Agent Marketplace"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./zyra_mesh.db"
    
    # AI Backend Providers
    DEFAULT_LLM_PROVIDER: str = "mock" # "ollama", "gemini", "mock"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_DEFAULT_MODEL: str = "qwen2.5:1.5b-instruct"
    GEMINI_API_KEY: str = ""
    GEMINI_DEFAULT_MODEL: str = "gemini-1.5-flash"
    
    # Execution & Trust Engine Settings
    DEFAULT_TRUST_MEAN: float = 0.5
    DEFAULT_TRUST_UNCERTAINTY: float = 0.5
    UNCERTAINTY_VERIFICATION_THRESHOLD: float = 0.4
    FAILURE_PROPAGATION_THRESHOLD: float = 0.6
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
