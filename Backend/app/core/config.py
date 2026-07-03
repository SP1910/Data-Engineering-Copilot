from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    # ==========================
    # Application Settings
    # ==========================
    app_name: str = "Data Engineering Copilot"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True

    # ==========================
    # Server Settings
    # ==========================
    host: str = "127.0.0.1"
    port: int = 8000

    # ==========================
    # API Settings
    # ==========================
    API_V1_STR: str = "/api/v1"

    # ==========================
    # Storage Settings
    # ==========================
    UPLOAD_DIR: str = "uploads"

    # ==========================
    # Database Settings
    # ==========================
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "data_engineering_copilot"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "password"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Returns the SQLAlchemy database connection URL.
        """
        return (
            f"postgresql+psycopg2://"
            f"{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
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