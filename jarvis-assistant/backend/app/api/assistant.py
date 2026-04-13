from fastapi import APIRouter, HTTPException
from app.models.schemas import TextRequest, AssistantResponse
from app.services.orchestrator import OrchestratorService

router = APIRouter(prefix="/assistant", tags=["Assistant"])

orchestrator = OrchestratorService()


@router.post("/chat", response_model=AssistantResponse)
async def chat_with_assistant(request: TextRequest):
    """
    Обработка текстовой команды пользователя
    
    Отправляет команду ассистенту и получает ответ.
    Поддерживает контекст через session_id.
    """
    try:
        response = await orchestrator.process_request(
            text=request.text,
            user_id=request.user_id,
            session_id=request.session_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice", response_model=AssistantResponse)
async def voice_command(request: TextRequest):
    """
    Обработка голосовой команды (текстовая версия для тестирования)
    
    В полной версии здесь будет прием аудиофайла или base64,
    его распознавание через STT сервис и последующая обработка.
    """
    # Пока работает как обычный чат, в будущем добавится STT
    return await chat_with_assistant(request)
