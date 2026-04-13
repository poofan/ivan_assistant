from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "healthy", "service": "ivan-assistant-backend"}


@router.get("/health/ready")
async def readiness_check():
    """Проверка готовности сервиса к обработке запросов"""
    # TODO: Добавить проверку подключений к БД и другим сервисам
    return {"status": "ready", "dependencies": "ok"}
