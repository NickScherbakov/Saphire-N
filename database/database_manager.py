import sqlite3
from typing import Any
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = "saphire.db"):
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