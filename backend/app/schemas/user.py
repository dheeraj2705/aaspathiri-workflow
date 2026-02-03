"""Pydantic schemas for User."""
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """Base user schema with common fields."""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user.
    
    Accepts password field for input validation, but it is NOT stored directly.
    Password hashing must be done in the application layer (Module 4: Auth).
    role_id is optional during creation (can be assigned separately or with default).
    """
    password: str  # Raw password from input, NOT stored
    role_id: int | None = None  # Optional - can be assigned after creation or via separate endpoint
    
    # Exclude password from response
    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    """Schema for reading a user from the database.
    
    NEVER exposes hashed_password to the client.
    """
    id: int
    username: str
    email: EmailStr
    is_active: bool
    role_id: int | None
    
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    username: str | None = None
    email: EmailStr | None = None
    role_id: int | None = None
    is_active: bool | None = None
    
    model_config = ConfigDict(from_attributes=True)
