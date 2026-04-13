from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class VoiceRequest(BaseModel):
    """Запрос на обработку голосовой команды"""
    audio_url: Optional[str] = Field(None, description="URL аудиофайла с командой")
    audio_base64: Optional[str] = Field(None, description="Аудио в base64 формате")
    text: Optional[str] = Field(None, description="Текстовая команда (если уже распознана)")
    user_id: str = Field(..., description="ID пользователя")
    session_id: Optional[str] = Field(None, description="ID сессии для контекста")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Иван, какая погода сейчас у меня",
                "user_id": "user_123",
                "session_id": "session_456"
            }
        }


class TextRequest(BaseModel):
    """Запрос на обработку текстовой команды"""
    text: str = Field(..., description="Текстовая команда")
    user_id: str = Field(..., description="ID пользователя")
    session_id: Optional[str] = Field(None, description="ID сессии для контекста")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Какая погода в Москве?",
                "user_id": "user_123"
            }
        }


class AssistantResponse(BaseModel):
    """Ответ ассистента"""
    text: str = Field(..., description="Текстовый ответ ассистента")
    audio_url: Optional[str] = Field(None, description="URL аудио с ответом (если TTS включен)")
    audio_base64: Optional[str] = Field(None, description="Аудио в base64 формате")
    action: Optional[str] = Field(None, description="Выполненное действие")
    data: Optional[Dict[str, Any]] = Field(None, description="Дополнительные данные")
    confidence: float = Field(0.95, description="Уверенность в ответе (0-1)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Сейчас у вас погода плюс шестнадцать градусов, ветрено",
                "action": "weather_check",
                "data": {
                    "temperature": 16,
                    "condition": "windy",
                    "location": "Москва"
                },
                "confidence": 0.98
            }
        }


class SkillResult(BaseModel):
    """Результат выполнения навыка"""
    skill_name: str
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class IntentClassification(BaseModel):
    """Классификация намерения пользователя"""
    intent: str = Field(..., description="Тип намерения")
    confidence: float = Field(..., description="Уверенность классификации")
    entities: Dict[str, Any] = Field(default_factory=dict, description="Извлеченные сущности")
    required_skills: List[str] = Field(default_factory=list, description="Необходимые навыки")
