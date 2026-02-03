"""Authentication API endpoints."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.deps import get_current_active_user, require_role
from app.auth.schemas import LoginRequest, RegisterRequest, Token, UserAuthResponse
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.db.deps import get_db
from app.models import User, Role

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=Token)
async def login(
    request: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    """Authenticate user and return JWT access token.

    Args:
        request: LoginRequest with username_or_email and password
        db: Database session

    Returns:
        Token with access_token and token_type

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == request.username_or_email)
        | (User.email == request.username_or_email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Verify password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Ensure user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    # Create JWT token
    # NOTE: Do NOT include role in token. Role is loaded from DB at request time.
    access_token = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserAuthResponse, status_code=201)
async def register(
    request: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
) -> UserAuthResponse:
    """Register a new user.

    Args:
        request: RegisterRequest with username, email, password, role_id
        db: Database session

    Returns:
        UserAuthResponse with user details (excluding password)

    Raises:
        HTTPException: 400 if user already exists or role_id invalid
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == request.username) | (User.email == request.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists with this username or email",
        )

    # Verify role exists
    role = db.query(Role).filter(Role.id == request.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role_id",
        )

    # Hash password and create user
    hashed_password = hash_password(request.password)
    new_user = User(
        username=request.username,
        email=request.email,
        hashed_password=hashed_password,
        is_active=True,
        role_id=request.role_id,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return user with role name
    return UserAuthResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        is_active=new_user.is_active,
        role_id=new_user.role_id,
        role_name=role.name,
    )


@router.get("/me", response_model=UserAuthResponse)
async def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
) -> UserAuthResponse:
    """Get current authenticated user.

    Args:
        current_user: Current authenticated user from dependency
        db: Database session

    Returns:
        UserAuthResponse with user details
    """
    # Refresh user to get latest data and role
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    role_name = user.role.name if user.role else None

    return UserAuthResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        role_id=user.role_id,
        role_name=role_name,
    )


@router.get("/admin-test")
async def admin_test(
    current_user: Annotated[User, Depends(require_role("admin"))],
) -> dict:
    """Test endpoint requiring admin role.

    This endpoint verifies that role-based access control works.
    Only admins can access this endpoint.

    Args:
        current_user: Admin user verified by require_role dependency

    Returns:
        Confirmation message
    """
    return {
        "message": "Admin access confirmed",
        "user": current_user.username,
        "user_id": current_user.id,
    }
