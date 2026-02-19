from typing import List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import deps
from app.core.security import get_password_hash
from app.models.users import User, UserRole
from app.schemas.users import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def list_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
) -> Any:
    """
    List all users (Admin only).
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
) -> Any:
    """
    Get a user by ID (Admin only).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
) -> Any:
    """
    Update a user (Admin only).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    else:
        update_data.pop("password", None)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/deactivate", response_model=UserSchema)
def deactivate_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
) -> Any:
    """
    Deactivate a user (soft delete via is_active=False). Admin only.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
