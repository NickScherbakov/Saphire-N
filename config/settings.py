import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Базовые настройки
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(BASE_DIR, "saphire.db"))

# OpenAI API настройки
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не установлен в .env файле")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1")

# Ollama API настройки
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
if not OLLAMA_API_KEY:
    raise ValueError("OLLAMA_API_KEY не установлен в .env файле")

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

# GigaChat API настройки
GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY")
if not GIGACHAT_API_KEY:
    raise ValueError("GIGACHAT_API_KEY не установлен в .env файле")

GIGACHAT_API_URL = os.getenv("GIGACHAT_API_URL", "https://api.gigachat.ai/v1")

# Google Search API настройки
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
if not GOOGLE_SEARCH_API_KEY:
    raise ValueError("GOOGLE_SEARCH_API_KEY не установлен в .env файле")

GOOGLE_CUSTOM_SEARCH_ID = os.getenv("GOOGLE_CUSTOM_SEARCH_ID")
if not GOOGLE_CUSTOM_SEARCH_ID:
    raise ValueError("GOOGLE_CUSTOM_SEARCH_ID не установлен в .env файле")

GOOGLE_API_URL = os.getenv("GOOGLE_API_URL", "https://www.googleapis.com/customsearch/v1")

# Настройки поиска
SEARCH_RESULTS_LIMIT = int(os.getenv("SEARCH_RESULTS_LIMIT", "10"))
SEARCH_TIMEOUT = int(os.getenv("SEARCH_TIMEOUT", "30"))

# Настройки логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.path.join(BASE_DIR, "logs", "saphire.log")

# Таймауты запросов (в секундах)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
ANALYSIS_TIMEOUT = int(os.getenv("ANALYSIS_TIMEOUT", "60"))
OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", "60")) 