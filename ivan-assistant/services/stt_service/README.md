# STT Service - Speech To Text

Сервис распознавания речи для ассистента "Иван".

## Возможности

- Распознавание аудио в текст
- Поддержка нескольких языков (RU, EN, DE, FR)
- Оценка уверенности распознавания
- REST API для интеграции

## API Endpoints

### GET /health
Проверка здоровья сервиса.

**Ответ:**
```json
{
  "status": "healthy",
  "service": "stt"
}
```

### POST /transcribe
Распознавание аудио файла.

**Параметры:**
- `file` (multipart/form-data): аудио файл (wav, mp3, ogg)
- `language` (query, optional): язык распознавания (по умолчанию "ru")

**Ответ:**
```json
{
  "success": true,
  "text": "какая сейчас погода",
  "confidence": 0.95,
  "language": "ru",
  "duration_seconds": 2.5
}
```

### GET /supported_languages
Получить список поддерживаемых языков.

**Ответ:**
```json
{
  "languages": [
    {"code": "ru", "name": "Русский"},
    {"code": "en", "name": "English"},
    {"code": "de", "name": "Deutsch"},
    {"code": "fr", "name": "Français"}
  ]
}
```

## Запуск

### Локально:
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002
```

### Docker:
```bash
docker-compose build stt-service
docker-compose up stt-service
```

## Интеграция с backend

Backend обращается к сервису по адресу: `http://stt-service:8002`

Пример использования из backend:
```python
import httpx

async def transcribe_audio(audio_bytes: bytes, language: str = "ru"):
    async with httpx.AsyncClient() as client:
        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        data = {"language": language}
        response = await client.post(
            "http://stt-service:8002/transcribe",
            files=files,
            data=data
        )
        return response.json()
```

## Будущие улучшения

- [ ] Интеграция с Vosk для локального распознавания
- [ ] Интеграция с Whisper.cpp для более точного распознавания
- [ ] Поддержка потокового распознавания
- [ ] Адаптация под голос пользователя
- [ ] Распознавание команд без активации (hotword detection)
