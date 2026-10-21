from abc import abstractmethod , ABC

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, system: str, user: str):
        """Generate SQL query from natural language prompt"""
        raise NotImplementedError
