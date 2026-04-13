from typing import Optional, Dict, Any
import logging

from app.models.schemas import AssistantResponse, IntentClassification
from app.services.llm_service import LLMService
from app.services.skills_service import SkillsService
from app.services.tts_service import TTSService

logger = logging.getLogger(__name__)


class OrchestratorService:
    """
    Оркестратор - центральный компонент системы
    
    Отвечает за:
    - Классификацию намерений пользователя
    - Маршрутизацию запросов к нужным сервисам
    - Управление контекстом диалога
    - Сборку финального ответа
    """
    
    def __init__(self):
        self.llm_service = LLMService()
        self.skills_service = SkillsService()
        self.tts_service = TTSService()
        self.context_store: Dict[str, list] = {}  # Временное хранение контекста

    async def process_request(
        self, 
        text: str, 
        user_id: str, 
        session_id: Optional[str] = None
    ) -> AssistantResponse:
        """
        Основной метод обработки запроса пользователя
        
        Args:
            text: Текст команды пользователя
            user_id: ID пользователя
            session_id: ID сессии для контекста
            
        Returns:
            AssistantResponse: Ответ ассистента
        """
        session_key = f"{user_id}:{session_id}" if session_id else user_id
        
        # 1. Классификация намерения
        intent = await self._classify_intent(text)
        logger.info(f"Классифицировано намерение: {intent.intent} (confidence: {intent.confidence})")
        
        # 2. Обновление контекста
        self._update_context(session_key, {"role": "user", "content": text})
        
        # 3. Выполнение необходимых навыков
        skill_result = None
        if intent.required_skills:
            skill_result = await self.skills_service.execute_skills(
                intent.required_skills,
                intent.entities,
                text
            )
        
        # 4. Генерация ответа через LLM
        response_text = await self._generate_response(
            text=text,
            intent=intent,
            skill_result=skill_result,
            context=self.context_store.get(session_key, [])
        )
        
        # 5. Обновление контекста ответом
        self._update_context(session_key, {"role": "assistant", "content": response_text})
        
        # 6. Формирование ответа
        response = AssistantResponse(
            text=response_text,
            action=intent.intent,
            data=skill_result.result if skill_result else None,
            confidence=intent.confidence
        )
        
        # 7. TTS (опционально, можно включить по флагу)
        # audio_url = await self.tts_service.synthesize(response_text)
        # response.audio_url = audio_url
        
        return response

    async def _classify_intent(self, text: str) -> IntentClassification:
        """Классификация намерения пользователя"""
        return await self.llm_service.classify_intent(text)

    async def _generate_response(
        self,
        text: str,
        intent: IntentClassification,
        skill_result: Optional[Dict],
        context: list
    ) -> str:
        """Генерация ответа ассистента"""
        return await self.llm_service.generate_response(
            user_input=text,
            intent=intent,
            skill_result=skill_result,
            context=context
        )

    def _update_context(self, session_key: str, message: Dict):
        """Обновление контекста диалога"""
        if session_key not in self.context_store:
            self.context_store[session_key] = []
        
        # Храним последние 10 сообщений для контекста
        self.context_store[session_key].append(message)
        if len(self.context_store[session_key]) > 10:
            self.context_store[session_key] = self.context_store[session_key][-10:]
