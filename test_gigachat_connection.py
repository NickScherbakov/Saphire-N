from gigachat import GigaChat
from dotenv import load_dotenv
import os

# Загружаем настройки из .env
load_dotenv()

def test_gigachat_connection():
    print("Тестирование подключения к GigaChat API...")
    
    try:
        # Получаем учетные данные из переменных окружения
        credentials = os.getenv("GIGACHAT_API_KEY")
        base_url = os.getenv("GIGACHAT_API_URL")
        model = os.getenv("GIGACHAT_MODEL")
        
        # Логирование переменных окружения
        print(f"GIGACHAT_API_KEY: {credentials}")
        print(f"GIGACHAT_API_URL: {base_url}")
        print(f"GIGACHAT_MODEL: {model}")
        
        if not credentials or not base_url:
            print("❌ Отсутствуют необходимые переменные окружения:")
            if not credentials:
                print("- GIGACHAT_API_KEY")
            if not base_url:
                print("- GIGACHAT_API_URL")
            return False
        
        print("\nПодключение к GigaChat...")
        with GigaChat(
            credentials=credentials,
            base_url=base_url,
            verify_ssl_certs=False,
            model=model
        ) as giga:
            print("✅ Подключение установлено")
            
            print("\nОтправка тестового запроса...")
            response = giga.chat("А это - мы! Твои тестовые тестировщики :-)")
            
            print("\n✅ Ответ получен:")
            print(response.choices[0].message.content)
            return True
            
    except Exception as e:
        print(f"\n❌ Произошла ошибка при тестировании:")
        print(f"Детали ошибки: {str(e)}")
        return False

if __name__ == "__main__":
    test_gigachat_connection()