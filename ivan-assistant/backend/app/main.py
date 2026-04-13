from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import health, assistant


def create_app() -> FastAPI:
    """Создание и настройка приложения FastAPI"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        description="Персональный голосовой ассистент Иван - микросервисная архитектура"
    )

    # Настройка CORS для мобильного приложения
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # В продакшене указать конкретные домены
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Регистрация роутов
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(assistant.router, prefix="/api/v1", tags=["Assistant"])

    @app.on_event("startup")
    async def startup_event():
        print(f"🚀 Запуск {settings.APP_NAME} v{settings.APP_VERSION}")
        print(f"📍 API доступно на http://{settings.HOST}:{settings.PORT}")

    @app.on_event("shutdown")
    async def shutdown_event():
        print(f"👋 Остановка {settings.APP_NAME}")

    return app


app = create_app()
