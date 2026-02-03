"""Database session management using SQLAlchemy."""
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


def _build_database_url() -> str:
    """Build PostgreSQL connection URL from settings."""
    # Use quote_plus to properly escape special characters in password
    password = quote_plus(settings.postgres_password.get_secret_value())
    return (
        f"postgresql+psycopg2://"
        f"{settings.postgres_user}:"
        f"{password}@"
        f"{settings.postgres_host}:"
        f"{settings.postgres_port}/"
        f"{settings.postgres_db}"
    )


DATABASE_URL = _build_database_url()

engine = create_engine(
    DATABASE_URL,
    echo=settings.debug,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

