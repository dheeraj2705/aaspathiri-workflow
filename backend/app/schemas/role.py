"""Pydantic schemas for Role."""
from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    """Base role schema with common fields."""
    name: str
    description: str | None = None


class RoleCreate(RoleBase):
    """Schema for creating a new role."""
    pass


class RoleRead(RoleBase):
    """Schema for reading a role from the database."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class RoleUpdate(RoleBase):
    """Schema for updating a role."""
    name: str | None = None
    description: str | None = None
