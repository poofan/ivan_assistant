from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Ivan Assistant"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "postgresql://ivan:ivan_password@localhost:5432/ivan_assistant"
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM Settings
    LOCAL_LLM_MODEL: str = "qwen2.5-3b"
    LOCAL_LLM_URL: str = "http://localhost:8001"
    CLOUD_LLM_URL: Optional[str] = None
    CLOUD_LLM_API_KEY: Optional[str] = None

    # STT Service
    STT_SERVICE_URL: str = "http://localhost:8002"

    # TTS Service
    TTS_SERVICE_URL: str = "http://localhost:8003"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
