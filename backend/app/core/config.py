from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, computed_field
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hospital Workflow Automation Portal"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "supersecretkeyneedschange"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "hospital_db"
    POSTGRES_PORT: int = 5432

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    class Config:
        case_sensitive = True

settings = Settings()
