import pytest
from unittest.mock import Mock, patch
import os
from dotenv import load_dotenv
from openai import OpenAI
from gigachat import GigaChat
import requests
import re

# Загружаем переменные окружения
load_dotenv()

# Получаем конфигурацию из переменных окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY")
GIGACHAT_API_URL = os.getenv("GIGACHAT_API_URL")
GIGACHAT_MODEL = os.getenv("MYGIGACHAT_MODEL")

class TestCooperativeBehavior:
    @pytest.fixture
    def setup_clients(self):
        """Инициализация реальных клиентов для каждой модели"""
        self.openai_client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_URL,
            timeout=60.0
        )
        
        self.gigachat_client = GigaChat(
            credentials=GIGACHAT_API_KEY,
            base_url=GIGACHAT_API_URL,
            verify_ssl_certs=False,
            model=GIGACHAT_MODEL
        )

    def get_model_response(self, client_type, prompt):
        """Получение ответа от конкретной модели"""
        try:
            if client_type == "openai":
                response = self.openai_client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content

            elif client_type == "ollama":
                response = requests.post(
                    f"{OLLAMA_API_URL}/api/generate",
                    json={
                        "model": OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                return response.json()["response"]

            elif client_type == "gigachat":
                response = self.gigachat_client.chat(prompt)
                return response.choices[0].message.content

        except Exception as e:
            return f"Ошибка при получении ответа от {client_type}: {str(e)}"

    def test_russian_dialogue(self, setup_clients):
        """Тест диалога между моделями на русском языке"""
        dialogue_history = []
        
        # Начальная тема для обсуждения
        topic = """
        Давайте обсудим важность сотрудничества между различными языковыми моделями 
        для решения сложных задач. Как мы можем наилучшим образом использовать сильные 
        стороны каждой модели?
        """
        
        dialogue_history.append(("Начальная тема", topic))
        
        # Последовательность моделей для диалога
        models = ["openai", "ollama", "gigachat"]
        
        for i in range(3):  # Три раунда обсуждения
            for model in models:
                # Формируем контекст из истории диалога
                context = "\n".join([f"{speaker}: {message}" for speaker, message in dialogue_history])
                
                prompt = f"""
                Контекст предыдущего обсуждения:
                {context}
                
                Пожалуйста, продолжите диалог, учитывая следующие требования:
                1. Ответ должен быть на русском языке
                2. Ответ должен быть связан с предыдущими сообщениями
                3. Внесите конструктивное предложение или идею
                4. Длина ответа - не более 2-3 предложений
                """
                
                response = self.get_model_response(model, prompt)
                dialogue_history.append((f"Модель {model}", response))
                
                # Проверяем ответ
                assert isinstance(response, str), f"Ответ от {model} должен быть строкой"
                assert len(response) > 0, f"Ответ от {model} не должен быть пустым"
                assert any(char.isalpha() for char in response), f"Ответ от {model} должен содержать буквы"
                
                # Проверяем наличие русских букв в ответе
                has_russian = bool(re.search('[а-яА-Я]', response))
                assert has_russian, f"Ответ от {model} должен быть на русском языке"
        
        # Выводим весь диалог
        print("\nПротокол диалога:")
        for speaker, message in dialogue_history:
            print(f"\n{speaker}:\n{message}")

    def test_task_solving_dialogue(self, setup_clients):
        """Тест совместного решения задачи моделями"""
        task = """
        Задача: Необходимо разработать концепцию образовательной платформы для детей.
        Каждая модель должна предложить свой аспект решения:
        1. Технический аспект
        2. Педагогический аспект
        3. Аспект пользовательского опыта
        """
        
        # Добавляем определение списка моделей
        models = ["openai", "ollama", "gigachat"]
        
        responses = {}
        aspects = {
            "openai": "технический аспект платформы",
            "ollama": "педагогический аспект платформы",
            "gigachat": "аспект пользовательского опыта"
        }
        
        for model, aspect in aspects.items():
            prompt = f"""
            {task}
            
            Пожалуйста, предложите решение для следующего аспекта: {aspect}
            
            Требования к ответу:
            1. Ответ должен быть на русском языке
            2. Предложите конкретное решение
            3. Объясните, как оно поможет в обучении детей
            4. Длина ответа - 2-3 предложения
            """
            
            response = self.get_model_response(model, prompt)
            responses[model] = response
            
            # Проверки ответа
            assert isinstance(response, str), f"Ответ от {model} должен быть строкой"
            assert len(response) > 0, f"Ответ от {model} не должен быть пустым"
            assert any(char.isalpha() for char in response), f"Ответ от {model} должен содержать буквы"
            
            # Проверка на русский язык
            has_russian = bool(re.search('[а-яА-Я]', response))
            assert has_russian, f"Ответ от {model} должен быть на русском языке"
            
            # Выводим полученные ответы для анализа
            print(f"\nОтвет от модели {model} по аспекту '{aspect}':")
            print(response)
        
        # Финальное обсуждение решений
        final_prompt = f"""
        Проанализируйте предложенные решения и предложите, как их можно объединить:
        
        Техническое решение: {responses['openai']}
        Педагогическое решение: {responses['ollama']}
        Решение по UX: {responses['gigachat']}
        
        Требования к ответу:
        1. Ответ должен быть на русском языке
        2. Предложите конкретный план объединения решений
        3. Укажите, какие преимущества даст такое объединение
        4. Длина ответа - 3-4 предложения
        """
        
        print("\nФинальное обсуждение решений:")
        for model in models:
            final_response = self.get_model_response(model, final_prompt)
            
            # Проверки финального ответа
            assert isinstance(final_response, str), f"Финальный ответ от {model} должен быть строкой"
            assert len(final_response) > 0, f"Финальный ответ от {model} не должен быть пустым"
            
            # Проверка на русский язык
            has_russian = bool(re.search('[а-яА-Я]', final_response))
            assert has_russian, f"Финальный ответ от {model} должен быть на русском языке"
            
            # Проверка содержательности ответа
            min_words = 20
            word_count = len(final_response.split())
            assert word_count >= min_words, f"Финальный ответ от {model} слишком короткий (меньше {min_words} слов)"
            
            # Выводим финальные ответы для анализа
            print(f"\nФинальный ответ от модели {model}:")
            print(final_response)
            
            # Сохраняем финальные ответы
            responses[f"{model}_final"] = final_response
        
        # Проверяем, что все модели предоставили различные ответы
        final_responses = [responses[f"{model}_final"] for model in models]
        assert len(set(final_responses)) == len(models), "Финальные ответы моделей не должны повторяться"
        
        print("\nТест успешно завершен: все модели предоставили уникальные содержательные ответы на русском языке")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])