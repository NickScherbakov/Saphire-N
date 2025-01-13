from openai import OpenAI
from typing import Dict, Any
from database.database_manager import DatabaseManager
from agents.ollama_agent import OllamaAgent
from agents.gigachat_agent import GigaChatAgent
from utils.logger import logger
import os
from dotenv import load_dotenv
import requests

# Загружаем настройки из .env
load_dotenv()

class OpenAIAssistant:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.ollama_agent = OllamaAgent()
        self.gigachat_agent = GigaChatAgent()
        
        # Настраиваем OpenAI клиент
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_URL"),
            timeout=60.0  # Устанавливаем таймаут в 60 секунд
        )
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
    def process_request(self, user_request: str) -> str:
        """
        Обработка запроса пользователя согласно диаграмме последовательности:
        1. Получение запроса
        2. Уточнение запроса
        3-4. Сохранение запроса и получение подтверждения
        5-6. Отправка задачи OllamaAgent и получение результатов анализа
        7-8. Отправка задачи GigaChatAgent и получение отчета
        9-10. Сохранение результатов и получение подтверждения
        11. Отправка ответа пользователю
        """
        try:
            # 2. Уточнение запроса
            clarified_request = self._clarify_request(user_request)
            
            # 3-4. Сохранение запроса в базе
            request_id = self.db_manager.save_request(clarified_request)
            
            # 5-6. Анализ данных через OllamaAgent
            analysis_results = self.ollama_agent.perform_task("analyze", clarified_request)
            
            # 7-8. Создание отчета через GigaChatAgent
            report = self.gigachat_agent.perform_task("create_report", analysis_results)
            
            # 9-10. Сохранение результатов
            self.db_manager.save_results(request_id, report)
            
            # 11. Возвращаем ответ пользователю
            return report
            
        except Exception as e:
            logger.error(f"Ошибка при обработке запроса: {str(e)}")
            raise

    def _clarify_request(self, request: str) -> str:
        """Уточнение запроса у пользователя через OpenAI"""
        try:
            # Формируем системный промпт для OpenAI
            messages = [
                {"role": "system", "content": """Ты - помощник, который уточняет запросы пользователей.
                Если запрос неясен или требует дополнительной информации, задай уточняющий вопрос.
                Если запрос ясен, просто подтверди его без изменений."""},
                {"role": "user", "content": request}
            ]
            
            # Отправляем запрос к OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            clarification = response.choices[0].message.content
            
            # Если это уточняющий вопрос, спрашиваем пользователя
            if "?" in clarification:
                print(f"\nУточнение: {clarification}")
                additional_info = input("Ваш ответ: ").strip()
                
                # Добавляем уточнение к диалогу
                messages.extend([
                    {"role": "assistant", "content": clarification},
                    {"role": "user", "content": additional_info}
                ])
                
                # Получаем финальную версию запроса
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                return final_response.choices[0].message.content
                
            return request  # Если уточнение не требуется
            
        except Exception as e:
            logger.error(f"Ошибка при уточнении запроса через OpenAI: {str(e)}")
            raise 

    def _route_request_to_agents(self, task: str) -> Dict[str, str]:
        # Пример логики маршрутизации
        if 'анализ' in task:
            result = self.ollama_agent.analyze(task)
            return {'OllamaAgent': result}
        else:
            result = self.gigachat_agent.create_report(task)
            return {'GigaChatAgent': result} 