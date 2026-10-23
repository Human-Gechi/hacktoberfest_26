from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-coder:3b"
    llm_temperature: float = 0.0
    database_url: str = "sqlite:///./examples/sample.db"
    sql_read_only: bool = True
    sql_execute_enabled: bool = True
    sql_query_timeout_seconds: int = 15
    sql_max_rows_returned: int = 100

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
