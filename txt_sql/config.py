from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-coder:3b"
    llm_temperature: float = 0.0
    database_url: str = f"sqlite:///{BASE_DIR / 'examples' / 'sample.db'}"
    sql_query_timeout_seconds: int = 15
    sql_max_rows_returned: int = 100
    dialect: str = "sqlite"

    @property
    def db_path(self) -> str:
        if self.database_url.startswith("sqlite:///"):
            return self.database_url.replace("sqlite:///", "", 1)
        return self.database_url

    @property
    def max_rows(self) -> int:
        return self.sql_max_rows_returned

    @property
    def timeout_s(self) -> int:
        return self.sql_query_timeout_seconds

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
