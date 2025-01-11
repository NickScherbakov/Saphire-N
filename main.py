from openai_assistant import OpenAIAssistant
from utils.logger import logger

def main():
    try:
        # Создаем экземпляр ассистента
        assistant = OpenAIAssistant()
        print("Система готова к работе!")
        print("Введите ваш запрос (для выхода введите 'exit'):")
        
        while True:
            # 1. Получаем запрос от пользователя
            request = input("\nВы: ").strip()
            
            if request.lower() == 'exit':
                print("Завершение работы...")
                break
                
            if not request:
                print("Запрос не может быть пустым")
                continue
            
            # Обрабатываем запрос согласно диаграмме последовательности
            response = assistant.process_request(request)
            print("\nОтвет:", response)
            
    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}")
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main() 