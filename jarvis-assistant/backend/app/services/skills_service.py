from typing import List, Dict, Any, Optional
import logging

from app.models.schemas import SkillResult

logger = logging.getLogger(__name__)


class SkillsService:
    """
    Сервис управления навыками (skills)
    
    Отвечает за выполнение конкретных действий:
    - Проверка погоды
    - Получение местоположения
    - Управление устройством
    - Поиск информации
    - Напоминания и т.д.
    """
    
    def __init__(self):
        # Регистрация доступных навыков
        self.skills = {
            "weather_skill": self._weather_skill,
            "time_skill": self._time_skill,
            "location_skill": self._location_skill,
            "reminder_skill": self._reminder_skill,
            "search_skill": self._search_skill,
            "device_control_skill": self._device_control_skill,
        }

    async def execute_skills(
        self,
        skill_names: List[str],
        entities: Dict[str, Any],
        user_input: str
    ) -> SkillResult:
        """
        Выполнение одного или нескольких навыков
        
        Args:
            skill_names: Список названий навыков для выполнения
            entities: Извлеченные сущности из запроса
            user_input: Исходный запрос пользователя
            
        Returns:
            SkillResult: Результат выполнения последнего навыка
        """
        result = None
        
        for skill_name in skill_names:
            if skill_name in self.skills:
                logger.info(f"Выполнение навыка: {skill_name}")
                try:
                    result = await self.skills[skill_name](entities, user_input)
                except Exception as e:
                    logger.error(f"Ошибка выполнения навыка {skill_name}: {e}")
                    result = SkillResult(
                        skill_name=skill_name,
                        success=False,
                        error=str(e)
                    )
            else:
                logger.warning(f"Навык {skill_name} не найден")
        
        return result or SkillResult(
            skill_name="unknown",
            success=False,
            error="No skills executed"
        )

    async def _weather_skill(self, entities: Dict, user_input: str) -> SkillResult:
        """Навык проверки погоды"""
        # Заглушка - в будущем будет вызов API погоды (OpenWeatherMap и т.п.)
        location = entities.get("location", "Москва")
        
        # Имитация ответа от API погоды
        return SkillResult(
            skill_name="weather_skill",
            success=True,
            result={
                "temperature": 16,
                "condition": "ветрено",
                "location": location,
                "humidity": 65,
                "wind_speed": 5.2
            }
        )

    async def _time_skill(self, entities: Dict, user_input: str) -> SkillResult:
        """Навык получения времени"""
        from datetime import datetime
        now = datetime.now()
        
        return SkillResult(
            skill_name="time_skill",
            success=True,
            result={
                "time": now.strftime("%H:%M"),
                "date": now.strftime("%d.%m.%Y"),
                "day_of_week": now.strftime("%A")
            }
        )

    async def _location_skill(self, entities: Dict, user_input: str) -> SkillResult:
        """Навык определения местоположения"""
        # Заглушка - в будущем будет GPS или IP-based геолокация
        return SkillResult(
            skill_name="location_skill",
            success=True,
            result={
                "latitude": 55.7558,
                "longitude": 37.6173,
                "address": "Москва, Россия",
                "city": "Москва"
            }
        )

    async def _reminder_skill(self, entities: Dict, user_input: str) -> SkillResult:
        """Навык создания напоминаний"""
        # Заглушка - в будущем будет интеграция с календарем
        return SkillResult(
            skill_name="reminder_skill",
            success=True,
            result={
                "message": "Напоминание создано",
                "time": "через 5 минут"
            }
        )

    async def _search_skill(self, entities: Dict, user_input: str) -> SkillResult:
        """Навык поиска информации"""
        # Заглушка - в будущем будет поисковый API
        return SkillResult(
            skill_name="search_skill",
            success=True,
            result={
                "query": user_input,
                "results_count": 3,
                "top_result": "Результат поиска по запросу"
            }
        )

    async def _device_control_skill(self, entities: Dict, user_input: str) -> SkillResult:
        """Навык управления устройством"""
        # Заглушка - в будущем будет управление функциями телефона
        return SkillResult(
            skill_name="device_control_skill",
            success=True,
            result={
                "action": "control",
                "message": "Команда выполнена"
            }
        )
