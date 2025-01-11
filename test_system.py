from openai_assistant import OpenAIAssistant
import sys

def test_simple_request():
    """Тест простого запроса"""
    print("Тестирование простого запроса...")
    assistant = OpenAIAssistant()
    
    try:
        assistant.initialize()
        print("✓ Система инициализирована")
        
        # Проверка возможностей агентов
        capabilities = assistant.query_agents_for_capabilities()
        print("\nДоступные возможности агентов:")
        for agent, caps in capabilities.items():
            print(f"- {agent}: {', '.join(caps)}")
        
        return assistant
    except Exception as e:
        print(f"✗ Ошибка при инициализации: {str(e)}")
        sys.exit(1)

def interactive_mode(assistant):
    """Интерактивный режим тестирования"""
    print("\nИнтерактивный режим (введите 'exit' для выхода)")
    print("Примеры запросов:")
    print("1. Найди информацию о последних достижениях в области искусственного интеллекта")
    print("2. Проанализируй тенденции развития Python за последний год")
    print("3. Сделай обзор современных фреймворков для машинного обучения")
    
    while True:
        try:
            request = input("\nВведите запрос: ")
            if request.lower() == 'exit':
                break
                
            if not request.strip():
                print("Запрос не может быть пустым")
                continue
            
            print("\nОбработка запроса...")
            result = assistant.handle_user_request(request)
            print("\nРезультат:")
            print("-" * 80)
            print(result)
            print("-" * 80)
            
        except KeyboardInterrupt:
            print("\nПрерывание работы...")
            break
        except Exception as e:
            print(f"Ошибка при обработке запроса: {str(e)}")

if __name__ == "__main__":
    print("=" * 80)
    print("Тестирование системы Saphire-N")
    print("=" * 80)
    
    # Инициализация и базовое тестирование
    assistant = test_simple_request()
    
    # Запуск интерактивного режима
    if assistant:
        interactive_mode(assistant) 