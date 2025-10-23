
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate
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
