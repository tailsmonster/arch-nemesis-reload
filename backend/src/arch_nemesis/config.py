from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Arch Nemesis: Reload"
    environment: str = "development"
    dry_run_mode: bool = False
    database_path: Path = Field(default=Path("../database/arch_nemesis.sqlite3"))
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.8
    llm_timeout_seconds: float = 30.0
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
