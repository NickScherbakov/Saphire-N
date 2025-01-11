import requests
from typing import List, Any, Dict
from .agent_interface import AgentInterface
from config.settings import OLLAMA_API_URL, REQUEST_TIMEOUT
from utils.logger import logger

class OllamaAgent(AgentInterface):
    def __init__(self):
        self.capabilities = ["text_analysis", "data_processing", "semantic_search"]
        self.api_url = OLLAMA_API_URL
    
    def get_capabilities(self) -> List[str]:
        return self.capabilities
    
    def perform_task(self, task_type: str, data: Any) -> Any:
        try:
            if task_type == "analyze":
                return self._analyze_data(data)
            raise ValueError(f"Неизвестный тип задачи: {task_type}")
        except Exception as e:
            logger.error(f"Ошибка при выполнении задачи {task_type}: {str(e)}")
            raise
    
    def _analyze_data(self, data: str) -> Dict[str, Any]:
        """Анализ данных с использованием Ollama"""
        try:
            response = requests.post(
                f"{self.api_url}/api/generate",
                json={
                    "model": "llama3.1",
                    "prompt": f"Analyze the following text and provide insights:\n{data}",
                    "stream": False
                },
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "analysis_result": result.get("response", ""),
                "confidence": 0.8,
                "model": "llama3.1"
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к Ollama API: {str(e)}")
            raise 