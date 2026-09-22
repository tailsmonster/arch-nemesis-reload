from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    dry_run_mode: bool = Field(default=True, alias="DRY_RUN_MODE")
    database_path: str = Field(default="arch_nemesis.sqlite3", alias="DATABASE_PATH")


@lru_cache
def get_settings() -> Settings:
    return Settings()
