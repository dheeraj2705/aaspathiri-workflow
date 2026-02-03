"""Password hashing and JWT token utilities."""
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing configuration using argon2 (Windows-compatible)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Role hierarchy (admin includes all permissions)
ROLE_HIERARCHY = {
    "admin": 4,
    "hr": 3,
    "doctor": 2,
    "staff": 1,
}


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    Args:
        password: Plaintext password to hash

    Returns:
        Hashed password string (bcrypt hash)
    """
    return pwd_context.hash(password)


def verify_password(plaintext_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hash.

    Args:
        plaintext_password: User-provided password
        hashed_password: Stored password hash from database

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plaintext_password, hashed_password)


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """Create a JWT access token.

    Args:
        data: Claims to encode in token (e.g., {"sub": "username"})
        expires_delta: Token expiration time. If None, uses default from settings

    Returns:
        Encoded JWT token string

    Note:
        Do NOT include role in token. Role is always loaded from database
        at request time to ensure permission changes are reflected immediately.
    """
    to_encode = data.copy()

    # Set expiration
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )

    to_encode.update({"exp": expire})

    # Encode JWT
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )

    return encoded_jwt


def decode_token(token: str) -> dict[str, Any] | None:
    """Decode and verify a JWT token.

    Args:
        token: JWT token string to decode

    Returns:
        Decoded token claims (dict) if valid, None if invalid or expired

    Raises:
        Nothing - returns None on any error to allow graceful handling
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        # Token invalid, expired, or tampered with
        return None


def can_access_role(user_role: str, required_role: str) -> bool:
    """Check if user's role can access a resource requiring a specific role.

    Admin role is a superset - admins can access everything.

    Args:
        user_role: User's current role
        required_role: Required role to access resource

    Returns:
        True if user can access, False otherwise
    """
    if user_role == "admin":
        # Admin can access everything
        return True

    user_level = ROLE_HIERARCHY.get(user_role, 0)
    required_level = ROLE_HIERARCHY.get(required_role, 0)

    return user_level >= required_level


def can_access_any_role(user_role: str, required_roles: list[str]) -> bool:
    """Check if user's role can access a resource requiring any of multiple roles.

    Admin role is a superset - admins can access everything.

    Args:
        user_role: User's current role
        required_roles: List of roles that can access resource

    Returns:
        True if user can access, False otherwise
    """
    if user_role == "admin":
        # Admin can access everything
        return True

    for required_role in required_roles:
        if can_access_role(user_role, required_role):
            return True

    return False
