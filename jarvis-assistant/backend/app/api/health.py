from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "healthy", "message": "Backend is running"}


@router.get("/health/ready")
async def readiness_check():
    """Проверка готовности сервиса к обработке запросов"""
    # Здесь можно добавить проверку подключений к БД, Redis и другим сервисам
    return {"status": "ready", "message": "Service is ready to accept requests"}
