from typing import Optional, Dict, Any, List
import logging
import random

from app.models.schemas import IntentClassification

logger = logging.getLogger(__name__)


class LLMService:
    """
    Сервис работы с языковой моделью
    
    В текущей версии использует заглушки для демонстрации.
    В будущем будет интегрирована локальная модель (Qwen2.5-3B, Phi-3-mini)
    или облачный API.
    """
    
    def __init__(self):
        # Примеры намерений и соответствующих навыков
        self.intent_patterns = {
            "weather": ["погода", "температура", "градус", "ветер", "дождь", "снег"],
            "greeting": ["привет", "здравствуй", "добрый день", "доброе утро"],
            "time": ["время", "который час", "сколько времени"],
            "location": ["где я", "мое местоположение", "адрес"],
            "reminder": ["напомни", "будильник", "напоминание"],
            "search": ["найди", "поиск", "гугл", "яндекс"],
            "control": ["включи", "выключи", "запусти", "открой"],
        }
        
        self.skill_mapping = {
            "weather": ["weather_skill"],
            "time": ["time_skill"],
            "location": ["location_skill"],
            "reminder": ["reminder_skill"],
            "search": ["search_skill"],
            "control": ["device_control_skill"],
        }

    async def classify_intent(self, text: str) -> IntentClassification:
        """
        Классификация намерения пользователя
        
        В полной версии здесь будет вызов локальной LLM модели
        для классификации текста и извлечения сущностей.
        """
        text_lower = text.lower()
        
        best_intent = "general_chat"
        best_confidence = 0.5
        entities = {}
        required_skills = []
        
        # Простая эвристическая классификация (заглушка)
        for intent, keywords in self.intent_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    best_intent = intent
                    best_confidence = 0.85 + random.uniform(0, 0.1)
                    required_skills = self.skill_mapping.get(intent, [])
                    
                    # Извлечение сущностей (упрощенно)
                    if intent == "weather":
                        entities["query_type"] = "weather"
                        # Здесь можно добавить распознавание города
                        if "москва" in text_lower:
                            entities["location"] = "Москва"
                        elif "спб" in text_lower or "санкт-петербург" in text_lower:
                            entities["location"] = "Санкт-Петербург"
                    break
        
        return IntentClassification(
            intent=best_intent,
            confidence=best_confidence,
            entities=entities,
            required_skills=required_skills
        )

    async def generate_response(
        self,
        user_input: str,
        intent: IntentClassification,
        skill_result: Optional[Dict],
        context: List[Dict]
    ) -> str:
        """
        Генерация ответа ассистента
        
        В полной версии здесь будет вызов LLM для генерации
        естественного ответа с учетом контекста и результатов навыков.
        """
        
        # Заглушка для демонстрации
        if intent.intent == "weather" and skill_result:
            temp = skill_result.result.get("temperature", 16) if skill_result.result else 16
            condition = skill_result.result.get("condition", "облачно") if skill_result.result else "облачно"
            location = skill_result.result.get("location", "вашем местоположении") if skill_result.result else "вашем местоположении"
            return f"Сейчас посмотрю... Сейчас у вас в {location} погода +{temp} градусов, {condition}."
        
        elif intent.intent == "greeting":
            greetings = [
                "Привет! Чем могу помочь?",
                "Здравствуйте! Готов к работе.",
                "Добрый день! Что нужно сделать?",
                "Приветствую! Жду ваших команд."
            ]
            return random.choice(greetings)
        
        elif intent.intent == "time":
            from datetime import datetime
            now = datetime.now().strftime("%H:%M")
            return f"Сейчас {now}."
        
        elif skill_result and skill_result.get("success"):
            return f"Выполнено: {skill_result.get('result', {})}"
        
        else:
            # Общий ответ для чата
            return f"Понял вас: '{user_input}'. Пока я учусь, но скоро смогу ответить лучше!"
