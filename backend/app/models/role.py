"""Role model for RBAC."""
from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from app.db.base import Base


class Role(Base):
    """Hospital staff role (Admin, HR, Doctor, Nurse, etc.)."""
    
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    
    # Relationship to users
    users = relationship("User", back_populates="role", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}')>"
