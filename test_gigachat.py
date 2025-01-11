from agents.gigachat_agent import GigaChatAgent
from utils.logger import logger

def test_gigachat():
    print("=" * 80)
    print("Тестирование GigaChat")
    print("=" * 80)
    
    try:
        # Создаем экземпляр агента
        agent = GigaChatAgent()
        print("✓ Агент создан")
        
        # Проверяем возможности
        capabilities = agent.get_capabilities()
        print("\nДоступные возможности:")
        print(", ".join(capabilities))
        
        # Тестовые данные для генерации отчета
        test_data = {
            "analysis_result": """
            Анализ показывает растущий интерес к технологиям искусственного интеллекта.
            Основные направления развития включают:
            1. Генеративные модели
            2. Мультимодальные системы
            3. Этичный ИИ
            
            Наблюдается значительный рост инвестиций в данную область.
            """,
            "confidence": 0.85,
            "model": "llama2"
        }
        
        print("\nГенерация тестового отчета...")
        report = agent.perform_task("create_report", test_data)
        
        print("\nСгенерированный отчет:")
        print("-" * 80)
        print(report)
        print("-" * 80)
        
        print("\n✓ Тест успешно завершен")
        
    except Exception as e:
        print(f"\n✗ Ошибка при тестировании: {str(e)}")
        logger.error(f"Ошибка при тестировании GigaChat: {str(e)}")

if __name__ == "__main__":
    test_gigachat() 