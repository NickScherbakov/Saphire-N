from typing import List, Any, Dict
from .agent_interface import AgentInterface
from config.settings import GIGACHAT_API_KEY, GIGACHAT_API_URL
from utils.logger import logger
from gigachat import GigaChat

class GigaChatAgent(AgentInterface):
    def __init__(self):
        self.capabilities = ["report_generation", "text_summarization", "visualization"]
        self.credentials = GIGACHAT_API_KEY
        self.base_url = GIGACHAT_API_URL
        self.model = "GigaChat-Pro-preview"
    
    def get_capabilities(self) -> List[str]:
        return self.capabilities
    
    def perform_task(self, task_type: str, data: Any) -> Any:
        try:
            if task_type == "create_report":
                return self._generate_report(data)
            raise ValueError(f"Неизвестный тип задачи: {task_type}")
        except Exception as e:
            logger.error(f"Ошибка при выполнении задачи {task_type}: {str(e)}")
            raise
    
    def _generate_report(self, data: Dict[str, Any]) -> str:
        """Генерация отчета на основе проанализированных данных"""
        try:
            # Формируем системный промпт
            system_prompt = """Вы - эксперт по созданию аналитических отчетов. 
            Ваша задача - создать подробный, структурированный отчет на основе предоставленных данных.
            Отчет должен быть информативным, логически организованным и легким для понимания."""
            
            # Формируем запрос для генерации отчета
            user_prompt = f"""Создайте подробный отчет на основе следующего анализа:
            
            Анализ данных:
            {data.get('analysis_result', '')}
            
            Уровень уверенности в анализе: {data.get('confidence', 'не указан')}
            Использованная модель: {data.get('model', 'не указана')}
            
            Пожалуйста, включите в отчет:
            1. Краткое резюме
            2. Основные выводы
            3. Детальный анализ
            4. Рекомендации (если применимо)"""
            
            # Используем контекстный менеджер для работы с GigaChat
            with GigaChat(
                credentials=self.credentials,
                base_url=self.base_url
            ) as giga:
                # Отправляем запрос
                response = giga.chat([
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ])
                
                # Получаем сгенерированный отчет
                report = response.choices[0].message.content
                
                logger.info("Отчет успешно сгенерирован через GigaChat")
                return report
                
        except Exception as e:
            logger.error(f"Ошибка при генерации отчета через GigaChat: {str(e)}")
            raise 