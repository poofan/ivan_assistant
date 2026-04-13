"""
STT Service - Speech To Text
Сервис распознавания речи для ассистента "Иван"
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import io
import logging
from typing import Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Ivan Assistant - STT Service",
    description="Сервис распознавания речи (Speech-to-Text)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "service": "stt"}

@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = "ru"
):
    """
    Распознавание аудио в текст
    
    Параметры:
    - file: аудио файл (wav, mp3, ogg)
    - language: язык распознавания (по умолчанию русский)
    
    Возвращает:
    - text: распознанный текст
    - confidence: уверенность распознавания (0-1)
    - language: использованный язык
    """
    try:
        # Чтение аудио файла
        audio_data = await file.read()
        
        if not audio_data:
            raise HTTPException(status_code=400, detail="Пустой аудио файл")
        
        # TODO: Интеграция с реальной STT моделью (Vosk/Whisper)
        # Пока возвращаем заглушку для тестирования
        
        logger.info(f"Получен аудио файл: {file.filename}, размер: {len(audio_data)} байт")
        
        # Заглушка для демонстрации
        response_text = "какая сейчас погода"
        confidence = 0.95
        
        return {
            "success": True,
            "text": response_text,
            "confidence": confidence,
            "language": language,
            "duration_seconds": 2.5
        }
        
    except Exception as e:
        logger.error(f"Ошибка распознавания: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка распознавания речи: {str(e)}")

@app.get("/supported_languages")
async def get_supported_languages():
    """Получить список поддерживаемых языков"""
    return {
        "languages": [
            {"code": "ru", "name": "Русский"},
            {"code": "en", "name": "English"},
            {"code": "de", "name": "Deutsch"},
            {"code": "fr", "name": "Français"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
