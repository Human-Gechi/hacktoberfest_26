from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openrouter_api_key: str = ""
    openrouter_model: str = "meta-llama/llama-3.2-3b-instruct:free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    llm_temperature: float = 0.0
    database_url: str = "sqlite:///./examples/sample.db"
    sql_read_only: bool = True
    sql_execute_enabled: bool = True
    sql_query_timeout_seconds: int = 15
    sql_max_rows_returned: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
