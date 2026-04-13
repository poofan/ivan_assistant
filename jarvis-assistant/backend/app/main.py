from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import health, assistant


def create_app() -> FastAPI:
    """Создание и настройка приложения FastAPI"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        description="Персональный голосовой ассистент в стиле Джарвис",
        version="0.1.0",
        debug=settings.DEBUG
    )

    # Настройка CORS для мобильного приложения
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # В продакшене заменить на конкретные домены
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Регистрация роутов
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(assistant.router, prefix="/api/v1", tags=["Assistant"])

    @app.get("/")
    async def root():
        return {
            "name": settings.APP_NAME,
            "version": "0.1.0",
            "status": "running"
        }

    return app


app = create_app()
