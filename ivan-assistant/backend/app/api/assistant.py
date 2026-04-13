from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class VoiceRequest(BaseModel):
    """Запрос на обработку голосовой команды"""
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    text: Optional[str] = None  # Для текстового ввода
    user_id: str = "default_user"


class VoiceResponse(BaseModel):
    """Ответ ассистента"""
    success: bool
    text_response: str
    audio_response_url: Optional[str] = None
    action_taken: Optional[str] = None
    confidence: float = 1.0


class CommandRequest(BaseModel):
    """Запрос на выполнение команды"""
    command: str
    parameters: Optional[dict] = None
    user_id: str = "default_user"


class CommandResponse(BaseModel):
    """Результат выполнения команды"""
    success: bool
    message: str
    data: Optional[dict] = None


@router.post("/voice/process", response_model=VoiceResponse)
async def process_voice(request: VoiceRequest):
    """
    Обработка голосового запроса
    
    1. Распознавание речи (STT)
    2. Анализ намерения (LLM Orchestrator)
    3. Выполнение действия
    4. Генерация ответа (LLM + TTS)
    """
    # TODO: Реализовать полный пайплайн обработки
    return VoiceResponse(
        success=True,
        text_response="Привет! Я Иван, ваш персональный ассистент. Чем могу помочь?",
        action_taken="greeting",
        confidence=0.95
    )


@router.post("/command/execute", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    Выполнение конкретной команды
    
    Примеры команд:
    - "погода" -> получение погоды
    - "напоминание" -> создание напоминания
    - "где я" -> определение местоположения
    """
    # TODO: Реализовать выполнение команд через сервис навыков
    return CommandResponse(
        success=True,
        message=f"Команда '{request.command}' принята в обработку",
        data={"command": request.command, "parameters": request.parameters}
    )


@router.get("/skills/list", response_model=List[str])
async def list_skills():
    """Получение списка доступных навыков"""
    # TODO: Заменить на реальный список из сервиса навыков
    return [
        "weather",
        "location",
        "reminder",
        "calendar",
        "search",
        "music_control",
        "device_control"
    ]


class ChatMessageRequest(BaseModel):
    """Запрос на сообщение в чате"""
    message: str
    user_id: str = "default_user"


@router.post("/chat/message")
async def chat_message(request: ChatMessageRequest):
    """
    Текстовый чат с ассистентом
    
    Прямое общение без голосового ввода
    """
    # TODO: Интеграция с LLM для генерации ответов
    return {
        "success": True,
        "response": f"Вы сказали: '{request.message}'. Я пока учусь, но скоро смогу ответить!",
        "user_id": request.user_id
    }
