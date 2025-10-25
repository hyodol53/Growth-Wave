
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate, UserUpdate
from app.crud import user as user_crud
from app.api import deps


router = APIRouter()

@router.post("/", response_model=User, status_code=201)
def create_user(
    *, 
    db: Session = Depends(get_db), 
    user_in: UserCreate, 
    current_user: UserModel = Depends(deps.get_current_admin_user)
):
    """
    Create new user. (Admin only)
    """
    user = user_crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = user_crud.user.create(db, obj_in=user_in)
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: UserModel = Depends(deps.get_current_admin_user),
):
    """
    Update a user. (Admin only)
    """
    user = user_crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = user_crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: UserModel = Depends(deps.get_current_admin_user),
):
    """
    Delete a user. (Admin only)
    """
    user = user_crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = user_crud.user.remove(db, id=user_id)
    return user
