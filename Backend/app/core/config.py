from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


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
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            database=self.DATABASE_NAME,
        ).render_as_string(hide_password=False)

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