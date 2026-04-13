from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Jarvis Assistant"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "postgresql://jarvis:jarvis_password@db:5432/jarvis_db"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # Services
    LLM_SERVICE_URL: str = "http://llm-service:8001"
    LLM_MODEL: str = "qwen2.5-3b"
    STT_SERVICE_URL: str = "http://stt-service:8002"
    TTS_SERVICE_URL: str = "http://tts-service:8003"
    SKILLS_SERVICE_URL: str = "http://skills-service:8004"

    # API Keys
    OPENWEATHER_API_KEY: Optional[str] = None
    GOOGLE_MAPS_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
