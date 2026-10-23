from ollama import Client

try:
    from txt_sql.config import Settings
    from txt_sql.llm.base import BaseLLM
except ImportError:
    from src.txt_sql.config import Settings
    from src.txt_sql.llm.base import BaseLLM


class OllamaLLM(BaseLLM):
    """LLM client using the official Ollama Python library."""

    def __init__(self, settings: Settings):
        self.model = settings.ollama_model
        self.client = Client(host=settings.ollama_base_url)
        self.options = {
            "temperature": settings.llm_temperature,
        }

    def generate(self, system: str, user: str) -> str:
        """Generate response from natural language prompt via Ollama."""
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            options=self.options,
        )
        if hasattr(response, "message") and hasattr(response.message, "content"):
            return response.message.content.strip()
        return response["message"]["content"].strip()
