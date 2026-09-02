"""Defines validated application configuration from environment variables.
Defaults support local development while secrets remain in an ignored `.env` file."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Hold process-wide settings with validation and safe local defaults."""

    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AI Job Seeking Assistant API"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    frontend_origin: str = "http://localhost:3000"
    database_url: str = (
        "postgresql+asyncpg://ai_job_assistant:change-me@localhost:5433/ai_job_assistant"
    )
    jobtech_base_url: str = "https://jobsearch.api.jobtechdev.se"
    jobtech_timeout_seconds: float = Field(default=20.0, gt=0, le=60)
    jobtech_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    """Build settings once so every request observes one consistent configuration."""
    return Settings()
