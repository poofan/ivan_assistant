# Ivan Assistant - Персональный голосовой ассистент

🤖 **Иван** - ваш персональный голосовой ассистент в стиле Джарвиса, работающий на Android и iOS.

## 🏗 Архитектура

Микросервисная архитектура с следующими компонентами:

- **Backend Core** (FastAPI) - API Gateway и оркестрация
- **STT Service** - распознавание речи
- **TTS Service** - синтез речи  
- **LLM Service** - работа с языковыми моделями
- **Skills Service** - внешние интеграции (погода, геолокация, etc.)
- **Mobile App** (Flutter) - кроссплатформенное приложение

## 🚀 Быстрый старт

### Требования
- Docker и Docker Compose
- Python 3.11+
- Postman (для тестирования API)

### Запуск через Docker Compose

```bash
cd ivan-assistant
docker-compose up -d
```

Сервисы будут доступны по адресам:
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Локальный запуск backend

```bash
cd ivan-assistant/backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## 📡 API Endpoints

### Health Checks
- `GET /api/v1/health` - проверка работоспособности
- `GET /api/v1/health/ready` - проверка готовности

### Assistant
- `POST /api/v1/voice/process` - обработка голосового запроса
- `POST /api/v1/command/execute` - выполнение команды
- `GET /api/v1/skills/list` - список доступных навыков
- `POST /api/v1/chat/message` - текстовый чат

## 🧪 Тестирование

Импортируйте коллекцию Postman из `docs/ivan-assistant.postman_collection.json` и тестируйте API.

## 📁 Структура проекта

```
ivan-assistant/
├── backend/              # Backend на FastAPI
│   ├── app/
│   │   ├── api/         # API роуты
│   │   ├── core/        # Конфигурация
│   │   ├── models/      # Модели данных
│   │   ├── services/    # Бизнес-логика
│   │   └── utils/       # Утилиты
│   ├── tests/           # Тесты
│   ├── requirements.txt
│   └── Dockerfile
├── services/            # Микросервисы
│   ├── llm/            # LLM сервис
│   ├── stt/            # STT сервис
│   └── tts/            # TTS сервис
├── mobile_app/          # Flutter приложение
├── docs/               # Документация
├── deploy/             # Деплой конфигурации
├── docker-compose.yml
└── PLAN.md            # План разработки
```

## 🛣 Roadmap

Смотрите [PLAN.md](PLAN.md) для детального плана разработки.

## 📝 Лицензия

MIT
