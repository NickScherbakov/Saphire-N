from openai import OpenAI
import os
from dotenv import load_dotenv

# Загружаем настройки из .env
load_dotenv()

def test_openai_connection():
    try:
        # Создаем клиент OpenAI с теми же настройками
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_URL"),
            timeout=60.0
        )
        
        # Пробуем сделать простой тестовый запрос
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "user", "content": "Привет, Коллега. Расскажите о себе. Подробно."}
            ]
        )
        
        # Если получили ответ - соединение работает
        if response.choices[0].message.content:
            print("✅ Подключение к OpenAI API успешно!")
            print(f"Ответ от API: {response.choices[0].message.content}")
            return True
            
    except Exception as e:
        print("❌ Ошибка при подключении к OpenAI API:")
        print(f"Детали ошибки: {str(e)}")
        
        # Проверяем наличие необходимых переменных окружения
        required_vars = ["OPENAI_API_KEY", "OPENAI_API_URL", "OPENAI_MODEL"]
        for var in required_vars:
            value = os.getenv(var)
            status = "✅ Установлена" if value else "❌ Отсутствует"
            print(f"Переменная {var}: {status}")
        
        return False

if __name__ == "__main__":
    test_openai_connection()
