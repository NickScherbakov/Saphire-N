from dotenv import load_dotenv
import os
from gigachat import GigaChat
import requests
from openai import OpenAI

# Загружаем настройки из .env
load_dotenv()

class AIModel:
    def __init__(self, name):
        self.name = name
        self.capabilities = None
        self.introduction = None

def test_cooperative_behavior():
    """Тест кооперативного поведения моделей"""
    print("\n=== Тестирование кооперативного поведения моделей ===")
    
    models = {
        'openai': AIModel('OpenAI'),
        'ollama': AIModel('Ollama'),
        'gigachat': AIModel('GigaChat')
    }
    
    # Этап 1: Знакомство - каждая модель представляется
    print("\n--- Этап 1: Знакомство моделей ---")
    
    # OpenAI представляется
    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_URL"),
            timeout=60.0
        )
        
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{
                "role": "user", 
                "content": "Представься кратко и опиши свои основные возможности для других языковых моделей."
            }]
        )
        models['openai'].introduction = response.choices[0].message.content
        print(f"\nOpenAI представляется:\n{models['openai'].introduction}")
        
    except Exception as e:
        print(f"❌ OpenAI: Ошибка - {str(e)}")

    # Ollama представляется
    try:
        OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        MODEL = os.getenv("OLLAMA_MODEL", "llama2")
        
        payload = {
            "model": MODEL,
            "prompt": "Представься кратко и опиши свои основные возможности для других языковых моделей.",
            "stream": False
        }
        
        response = requests.post(
            f"{OLLAMA_API_URL}/api/generate",
            json=payload
        )
        
        if response.status_code == 200:
            models['ollama'].introduction = response.json().get('response', '')
            print(f"\nOllama представляется:\n{models['ollama'].introduction}")
            
    except Exception as e:
        print(f"❌ Ollama: Ошибка - {str(e)}")

    # GigaChat представляется
    try:
        with GigaChat(
            credentials=os.getenv("GIGACHAT_CREDENTIALS"),
            base_url=os.getenv("GIGACHAT_API_URL"),
            verify_ssl_certs=False,
            model=os.getenv("MYGIGACHAT_MODEL", "GigaChat")  # Исправлено название переменной
        ) as giga:
            response = giga.chat("Представься кратко и опиши свои основные возможности для других языковых моделей.")
            models['gigachat'].introduction = response.choices[0].message.content
            print(f"\nGigaChat представляется:\n{models['gigachat'].introduction}")
            
    except Exception as e:
        print(f"❌ GigaChat: Ошибка - {str(e)}")

    # Этап 2: Анализ возможностей друг друга
    print("\n--- Этап 2: Анализ возможностей ---")
    
    # OpenAI анализирует других
    try:
        messages = [
            {"role": "system", "content": "Проанализируй представления других моделей и выдели их ключевые особенности."},
            {"role": "user", "content": f"Ollama: {models['ollama'].introduction}\nGigaChat: {models['gigachat'].introduction}"}
        ]
        
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=messages
        )
        print(f"\nOpenAI анализирует других:\n{response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ OpenAI анализ: Ошибка - {str(e)}")

    # GigaChat анализирует других
    try:
        with GigaChat(
            credentials=os.getenv("GIGACHAT_CREDENTIALS"),
            base_url=os.getenv("GIGACHAT_API_URL"),
            verify_ssl_certs=False,
            model=os.getenv("MYGIGACHAT_MODEL", "GigaChat")  # Исправлено название переменной
        ) as giga:
            prompt = f"Проанализируй представления других моделей и выдели их ключевые особенности:\nOpenAI: {models['openai'].introduction}\nOllama: {models['ollama'].introduction}"
            response = giga.chat(prompt)
            print(f"\nGigaChat анализирует других:\n{response.choices[0].message.content}")
            
    except Exception as e:
        print(f"❌ GigaChat анализ: Ошибка - {str(e)}")

    # Этап 3: Предложение кооперации
    print("\n--- Этап 3: Предложение кооперации ---")
    
    try:
        messages = [
            {"role": "system", "content": "На основе знаний о возможностях всех моделей, предложи оптимальный способ их взаимодействия для решения сложных задач."},
            {"role": "user", "content": f"Модели и их возможности:\nOpenAI: {models['openai'].introduction}\nOllama: {models['ollama'].introduction}\nGigaChat: {models['gigachat'].introduction}"}
        ]
        
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=messages
        )
        print(f"\nПредложение по кооперации:\n{response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ Анализ кооперации: Ошибка - {str(e)}")

if __name__ == "__main__":
    print("Начало тестирования кооперативного поведения моделей...")
    test_cooperative_behavior()
    print("\nТестирование завершено")
