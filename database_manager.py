import sqlite3
from typing import Any, Dict
from pathlib import Path
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path: str = "saphire.db"):
        """Инициализация менеджера базы данных"""
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Инициализация структуры базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Создание таблицы запросов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Создание таблицы результатов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER,
                result_data TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (request_id) REFERENCES requests (id)
            )
        ''')
        
        # Создание таблицы для разговоров моделей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_type TEXT NOT NULL,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Создание таблицы для сообщений моделей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                model_name TEXT NOT NULL,
                message_type TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES model_conversations (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_request(self, request: str) -> int:
        """Сохранение запроса пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO requests (request_text) VALUES (?)', (request,))
        request_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return request_id
    
    def save_results(self, request_id: int, results: Any) -> None:
        """Сохранение результатов обработки"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO results (request_id, result_data) VALUES (?, ?)',
            (request_id, str(results))
        )
        
        conn.commit()
        conn.close()
    
    def save_model_conversation(self, conversation_type: str) -> int:
        """Создание новой записи о разговоре моделей"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO model_conversations (conversation_type) VALUES (?)',
            (conversation_type,)
        )
        conversation_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return conversation_id
    
    def save_model_message(self, conversation_id: int, model_name: str, 
                          message_type: str, content: Any) -> None:
        """Сохранение сообщения модели"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Преобразуем контент в JSON, если это словарь или список
        if isinstance(content, (dict, list)):
            content = json.dumps(content, ensure_ascii=False)
        else:
            content = str(content)
        
        cursor.execute(
            '''INSERT INTO model_messages 
               (conversation_id, model_name, message_type, content) 
               VALUES (?, ?, ?, ?)''',
            (conversation_id, model_name, message_type, content)
        )
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, conversation_id: int) -> list:
        """Получение истории разговора"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            '''SELECT model_name, message_type, content, timestamp 
               FROM model_messages 
               WHERE conversation_id = ? 
               ORDER BY timestamp''',
            (conversation_id,)
        )
        
        history = cursor.fetchall()
        conn.close()
        
        return [
            {
                'model_name': row[0],
                'message_type': row[1],
                'content': row[2],
                'timestamp': row[3]
            }
            for row in history
        ]
    
    def close_conversation(self, conversation_id: int) -> None:
        """Закрытие разговора"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            '''UPDATE model_conversations 
               SET status = 'completed', end_time = CURRENT_TIMESTAMP 
               WHERE id = ?''',
            (conversation_id,)
        )
        
        conn.commit()
        conn.close()