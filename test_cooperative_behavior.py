import pytest
from unittest.mock import Mock, patch
import os
from dotenv import load_dotenv
from openai import OpenAI
from gigachat import GigaChat
import requests
import re
import datetime
import sqlite3
from contextlib import contextmanager

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

# Конфигурация для БД
DATABASE_PATH = "saphire.db"

@contextmanager
def get_db_connection():
    """Контекстный менеджер для работы с БД"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Инициализация таблиц для хранения диалогов"""
    with get_db_connection() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS model_dialogues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_name TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model_name TEXT NOT NULL,
            message_type TEXT NOT NULL,
            message_content TEXT NOT NULL,
            aspect TEXT,
            sequence_number INTEGER NOT NULL
        )
        ''')
        conn.commit()

class TestCooperativeBehavior:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Общая фикстура для настройки всего необходимого"""
        # Инициализация БД
        init_db()
        
        # Инициализация клиентов
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
        
        yield
        
        # Очистка после тестов
        if hasattr(self, 'gigachat_client'):
            self.gigachat_client.close()

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

    def save_dialogue_to_db(self, test_name, dialogue_entries):
        """Сохранение диалога в базу данных"""
        with get_db_connection() as conn:
            for seq_num, entry in enumerate(dialogue_entries):
                conn.execute('''
                INSERT INTO model_dialogues 
                (test_name, model_name, message_type, message_content, aspect, sequence_number)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    test_name,
                    entry.get('model', 'system'),
                    entry.get('type', 'message'),
                    entry['content'],
                    entry.get('aspect'),
                    seq_num
                ))
            conn.commit()

    def get_dialogue_from_db(self, test_name):
        """Получение диалога из базы данных"""
        with get_db_connection() as conn:
            return conn.execute('''
                SELECT * FROM model_dialogues 
                WHERE test_name = ? 
                ORDER BY sequence_number
                ''', (test_name,)).fetchall()

    def print_dialogue_section(self, title, content):
        """Красиво выводит секцию диалога"""
        print("\n" + "=" * 80)
        print(f" {title} ".center(80, "="))
        print("=" * 80)
        print(content)
        print("-" * 80)

    def test_russian_dialogue(self):
        """Тест диалога между моделями на русском языке"""
        dialogue_entries = []
        test_name = f"russian_dialogue_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Начальная тема
        topic = """
        Давайте обсудим важность сотрудничества между различными языковыми моделями 
        для решения сложных задач. Как мы можем наилучшим образом использовать сильные 
        стороны каждой модели?
        """
        
        dialogue_entries.append({
            'model': 'system',
            'type': 'topic',
            'content': topic
        })
        
        models = ["openai", "ollama", "gigachat"]
        
        for i in range(3):
            for model in models:
                context = "\n".join([entry['content'] for entry in dialogue_entries])
                
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
                
                # Проверки ответа
                assert isinstance(response, str), f"Ответ от {model} должен быть строкой"
                assert len(response) > 0, f"Ответ от {model} не должен быть пустым"
                assert any(char.isalpha() for char in response), f"Ответ от {model} должен содержать буквы"
                has_russian = bool(re.search('[а-яА-Я]', response))
                assert has_russian, f"Ответ от {model} должен быть на русском языке"
                
                dialogue_entries.append({
                    'model': model,
                    'type': 'response',
                    'content': response
                })
                
                self.print_dialogue_section(f"Ответ от модели {model}", response)
        
        # Сохраняем диалог в БД
        self.save_dialogue_to_db(test_name, dialogue_entries)

    def test_task_solving_dialogue(self):
        """Тест совместного решения задачи моделями"""
        dialogue_entries = []
        test_name = f"task_solving_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        task = """
        Задача: Необходимо разработать концепцию образовательной платформы для детей.
        Каждая модель должна предложить свой аспект решения:
        1. Технический аспект
        2. Педагогический аспект
        3. Аспект пользовательского опыта
        """
        
        dialogue_entries.append({
            'model': 'system',
            'type': 'task',
            'content': task
        })
        
        models = ["openai", "ollama", "gigachat"]
        aspects = {
            "openai": "технический аспект платформы",
            "ollama": "педагогический аспект платформы",
            "gigachat": "аспект пользовательского опыта"
        }
        
        responses = {}
        
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
            
            dialogue_entries.append({
                'model': model,
                'type': 'aspect_response',
                'content': response,
                'aspect': aspect
            })
            
            # Проверки ответа
            assert isinstance(response, str), f"Ответ от {model} должен быть строкой"
            assert len(response) > 0, f"Ответ от {model} не должен быть пустым"
            assert any(char.isalpha() for char in response), f"Ответ от {model} должен содержать буквы"
            has_russian = bool(re.search('[а-яА-Я]', response))
            assert has_russian, f"Ответ от {model} должен быть на русском языке"
            
            self.print_dialogue_section(f"Ответ от модели {model} по аспекту '{aspect}'", response)
        
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
            
            dialogue_entries.append({
                'model': model,
                'type': 'final_response',
                'content': final_response
            })
            
            # Проверки финального ответа
            assert isinstance(final_response, str), f"Финальный ответ от {model} должен быть строкой"
            assert len(final_response) > 0, f"Финальный ответ от {model} не должен быть пустым"
            has_russian = bool(re.search('[а-яА-Я]', final_response))
            assert has_russian, f"Финальный ответ от {model} должен быть на русском языке"
            
            # Проверка содержательности ответа
            min_words = 20
            word_count = len(final_response.split())
            assert word_count >= min_words, f"Финальный ответ от {model} слишком короткий (меньше {min_words} слов)"
            
            self.print_dialogue_section(f"Финальный ответ от модели {model}", final_response)
            responses[f"{model}_final"] = final_response
        
        # Сохраняем весь диалог в БД
        self.save_dialogue_to_db(test_name, dialogue_entries)
        
        # Проверяем, что все модели предоставили различные ответы
        final_responses = [responses[f"{model}_final"] for model in models]
        assert len(set(final_responses)) == len(models), "Финальные ответы моделей не должны повторяться"
        
        print("\nТест успешно завершен: все модели предоставили уникальные содержательные ответы на русском языке")

def view_latest_test_results():
    """Просмотр последних результатов тестов"""
    with get_db_connection() as conn:
        # Последние тесты
        latest_tests = conn.execute('''
            SELECT DISTINCT test_name, timestamp 
            FROM model_dialogues 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''').fetchall()
        
        for test in latest_tests:
            print(f"\n=== Тест: {test['test_name']} ===")
            print(f"Время: {test['timestamp']}")
            
            # Сообщения в тесте
            messages = conn.execute('''
                SELECT model_name, message_type, message_content, aspect
                FROM model_dialogues
                WHERE test_name = ?
                ORDER BY sequence_number
            ''', (test['test_name'],)).fetchall()
            
            for msg in messages:
                print(f"\nМодель: {msg['model_name']}")
                if msg['aspect']:
                    print(f"Аспект: {msg['aspect']}")
                print(f"Тип: {msg['message_type']}")
                print(f"Сообщение: {msg['message_content']}")
                print("-" * 40)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])