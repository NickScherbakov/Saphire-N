from abc import ABC, abstractmethod
from typing import List, Any

class AgentInterface(ABC):
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Возвращает список возможностей агента"""
        pass
    
    @abstractmethod
    def perform_task(self, task_type: str, data: Any) -> Any:
        """Выполняет задачу определенного типа"""
        pass 