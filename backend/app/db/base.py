"""SQLAlchemy ORM declarative base for all models."""
from sqlalchemy.orm import declarative_base

# All ORM models should inherit from this Base class
Base = declarative_base()
