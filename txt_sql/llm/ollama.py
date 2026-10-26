from ollama import Client

from txt_sql.config import Settings
from txt_sql.config import settings as default_settings
from txt_sql.llm.base import BaseLLM


class OllamaLLM(BaseLLM):
    """LLM client using the official Ollama Python library."""

    def __init__(self, settings: Settings | None = None):
        cfg = settings or default_settings
        self.model = cfg.ollama_model
        self.client = Client(host=cfg.ollama_base_url)
        self.options = {
            "temperature": cfg.llm_temperature,
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
