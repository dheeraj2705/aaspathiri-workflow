"""Import all SQLAlchemy models to ensure they are registered with the Base."""
from app.models.role import Role
from app.models.user import User
from app.models.appointment import Appointment

__all__ = ["Role", "User", "Appointment"]
