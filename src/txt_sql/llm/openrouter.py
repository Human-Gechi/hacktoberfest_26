import requests

try:
    from txt_sql.llm.base import BaseLLM
    from txt_sql.config import Settings
except ImportError:
    from src.txt_sql.llm.base import BaseLLM
    from src.txt_sql.config import Settings


class OpenRouterLLM(BaseLLM):

    def __init__(self, settings: Settings):
        self.api_key = settings.openrouter_api_key
        self.model = settings.openrouter_model
        self.base_url = settings.openrouter_base_url.rstrip("/")
        self.temperature = settings.llm_temperature
        self.timeout = settings.sql_query_timeout_seconds

    def generate(self, system: str, user: str) -> str:
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key is missing! Please set OPENROUTER_API_KEY in your .env file."
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "txt_sql"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": self.temperature
        }

        response = requests.post(
            url=f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=self.timeout
        )

        if response.status_code != 200:
            raise Exception(f"Error calling OpenRouter API ({response.status_code}): {response.text}")

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()


