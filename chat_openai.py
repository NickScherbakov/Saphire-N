import openai
from dotenv import load_dotenv
import os

# Загружаем настройки из .env
load_dotenv()

# Настраиваем клиент OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_URL")

def chat_with_openai():
    print("Начинаем диалог с OpenAI (для выхода введите 'exit')")
    print("-" * 50)
    
    while True:
        # Получаем ввод пользователя
        user_input = input("\nВы: ")
        
        if user_input.lower() == 'exit':
            print("Завершение работы...")
            break
            
        try:
            # Отправляем запрос к API
            response = openai.ChatCompletion.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            
            # Выводим ответ
            assistant_response = response.choices[0].message.content
            print("\nAssistant:", assistant_response)
            
        except Exception as e:
            print(f"\nОшибка при получении ответа: {str(e)}")

if __name__ == "__main__":
    chat_with_openai() 