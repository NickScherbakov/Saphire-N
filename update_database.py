import sqlite3
import os
from pathlib import Path

def update_database():
    """Обновление структуры базы данных"""
    db_path = "saphire.db"
    
    # Если база существует, сделаем резервную копию
    if os.path.exists(db_path):
        backup_path = db_path + ".backup"
        print(f"Создание резервной копии базы данных: {backup_path}")
        import shutil
        shutil.copy2(db_path, backup_path)
    
    print("Обновление структуры базы данных...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Создаем новые таблицы
        print("Создание таблицы model_conversations...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_type TEXT NOT NULL,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        print("Создание таблицы model_messages...")
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
        print("✅ Структура базы данных успешно обновлена")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Ошибка при обновлении базы данных: {str(e)}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    update_database()
