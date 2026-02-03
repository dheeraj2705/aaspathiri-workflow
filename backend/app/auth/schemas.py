"""Pydantic schemas for authentication endpoints."""
from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
    """Request body for login endpoint."""

    username_or_email: str
    password: str


class RegisterRequest(BaseModel):
    """Request body for registration endpoint."""

    username: str
    email: EmailStr
    password: str
    role_id: int


class Token(BaseModel):
    """Response body for token endpoint."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Decoded JWT token data."""

    sub: str | None = None


class UserAuthResponse(BaseModel):
    """User data returned in authenticated responses.

    Deliberately excludes sensitive fields like hashed_password.
    """

    id: int
    username: str
    email: EmailStr
    is_active: bool
    role_id: int | None = None
    role_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
