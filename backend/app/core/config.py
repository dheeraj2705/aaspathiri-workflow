from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file.

    Keep this module import-safe and side-effect free. Use the cached
    `settings` object when reading configuration across the app.
    """

    # App settings
    app_name: str = "Hospital Workflow Backend"
    app_env: str = "development"
    debug: bool = False
    secret_key: SecretStr

    # PostgreSQL settings
    postgres_user: str = "postgres"
    postgres_password: SecretStr
    postgres_db: str = "hospital_workflow"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # JWT settings
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    # Resolve the .env file relative to the backend package root so loading
    # works whether the package is imported from the project root or when
    # PYTHONPATH points to the backend folder.
    _backend_root = Path(__file__).resolve().parents[2]
    model_config = SettingsConfigDict(
        env_file=str(_backend_root / ".env"), env_file_encoding="utf-8"
    )

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() in ("prod", "production")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
