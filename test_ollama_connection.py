import requests
import os
from dotenv import load_dotenv
import json

# Загружаем настройки из .env
load_dotenv()

def test_ollama_connection():
    # Получаем URL из переменной окружения или используем значение по умолчанию
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    MODEL = os.getenv("OLLAMA_MODEL", "llama2")  # Модель по умолчанию
    
    print(f"Тестирование подключения к Ollama API...")
    print(f"URL API: {OLLAMA_API_URL}")
    print(f"Модель: {MODEL}")
    
    try:
        # Проверяем доступные модели
        models_response = requests.get(f"{OLLAMA_API_URL}/api/tags")
        if models_response.status_code == 200:
            print("\n✅ Соединение с Ollama API установлено!")
            models = models_response.json()
            print("\nДоступные модели:")
            for model in models['models']:
                print(f"- {model['name']}")
        
        # Пробуем отправить тестовый запрос
        test_prompt = "Привет! Пожалуйста, расскажите о себе. Подробно."
        
        payload = {
            "model": MODEL,
            "prompt": test_prompt,
            "stream": False
        }
        
        print(f"\nОтправка тестового запроса к модели {MODEL}...")
        
        response = requests.post(
            f"{OLLAMA_API_URL}/api/generate",
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Тестовый запрос успешно обработан!")
            print(f"\nОтвет от модели: {result.get('response', '')}")
            return True
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Ошибка подключения к {OLLAMA_API_URL}")
        print("Убедитесь, что:")
        print("1. Ollama запущена")
        print("2. URL API указан верно")
        print("3. Порт 11434 доступен")
        return False
        
    except Exception as e:
        print("\n❌ Произошла ошибка при тестировании:")
        print(f"Детали ошибки: {str(e)}")
        
        # Проверяем наличие необходимых переменных окружения
        required_vars = ["OLLAMA_API_URL", "OLLAMA_MODEL"]
        for var in required_vars:
            value = os.getenv(var)
            status = "✅ Установлена" if value else "❌ Отсутствует"
            print(f"Переменная {var}: {status}")
        return False

if __name__ == "__main__":
    test_ollama_connection()
