from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    app_name: str = "Data Engineering Copilot"
    app_version: str = "0.1.0"

    environment: str = "development"

    debug: bool = True

    host: str = "127.0.0.1"

    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    The configuration is loaded only once during the application's lifetime.
    """
    return Settings()


settings = get_settings()