"""Authentication and authorization dependencies for FastAPI routes.

These dependencies enforce:
1. User authentication (valid JWT token)
2. User is active
3. Role-based access control (RBAC) with admin hierarchy
"""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from starlette.authentication import AuthCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_token, can_access_role, can_access_any_role
from app.db.deps import get_db
from app.models import User
from app.auth.schemas import TokenData

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[AuthCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """Extract and validate the current user from JWT token.

    Decodes JWT, loads user from database, and returns User object.
    If token is invalid, expired, or user is not found, raises 401.

    Args:
        credentials: HTTP Bearer credentials from request
        db: Database session

    Returns:
        User object loaded from database

    Raises:
        HTTPException: 401 if token invalid or user not found
    """
    token = credentials.credentials

    # Decode and validate token
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract username from token
    username: str | None = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Load user from database
    user = db.query(User).filter(
        (User.username == username) | (User.email == username)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Ensure current user is active.

    Args:
        current_user: User from get_current_user dependency

    Returns:
        User object if active

    Raises:
        HTTPException: 403 if user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return current_user


def require_role(required_role: str):
    """Dependency factory for role-based access control.

    Ensures current user has the required role or is admin (admin is superset).

    Args:
        required_role: Role name required to access resource (e.g., "hr", "doctor")

    Returns:
        FastAPI dependency that validates role

    Example:
        @router.get("/admin-only", dependencies=[Depends(require_role("admin"))])
        async def admin_endpoint(current_user: User = Depends(get_current_active_user)):
            return {"message": "Admin access"}
    """

    async def check_role(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Annotated[Session, Depends(get_db)],
    ) -> User:
        # Load user's role
        user_role = db.query(User).filter(User.id == current_user.id).first()
        if not user_role or not user_role.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role not found",
            )

        # Check if user's role can access required role
        if not can_access_role(user_role.role.name, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role}",
            )

        return current_user

    return check_role


def require_roles(required_roles: list[str]):
    """Dependency factory for multi-role access control.

    Ensures current user has at least one of the required roles or is admin.

    Args:
        required_roles: List of role names (user needs at least one)

    Returns:
        FastAPI dependency that validates roles

    Example:
        @router.get(
            "/doctor-or-hr",
            dependencies=[Depends(require_roles(["doctor", "hr"]))]
        )
        async def multi_role_endpoint(current_user: User = Depends(get_current_active_user)):
            return {"message": "Access granted"}
    """

    async def check_roles(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Annotated[Session, Depends(get_db)],
    ) -> User:
        # Load user's role
        user_obj = db.query(User).filter(User.id == current_user.id).first()
        if not user_obj or not user_obj.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role not found",
            )

        # Check if user's role can access any of the required roles
        if not can_access_any_role(user_obj.role.name, required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required one of: {', '.join(required_roles)}",
            )

        return current_user

    return check_roles
