from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel, UserRole
from app.schemas.user import User, UserCreate, UserUpdate, UserHistoryResponse
from app.schemas.project_member import (
    ProjectMemberWeightDetail,
    UserProjectWeightsUpdate,
)
from app.crud import user as user_crud
from app.crud import project_member as project_member_crud
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


@router.get("/me", response_model=User)
def read_current_user(
    current_user: UserModel = Depends(deps.get_current_user),
):
    """
    Retrieve current authenticated user.
    """
    return current_user


@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_admin_or_dept_head_user),
):
    """
    Retrieve users.
    - Admins can retrieve all users.
    - Department Heads can retrieve their subordinates.
    """
    if current_user.role == UserRole.ADMIN:
        users = user_crud.user.get_multi(db)
    elif current_user.role == UserRole.DEPT_HEAD:
        users = user_crud.user.get_subordinates(db, user_id=current_user.id)
    else:
        # This case should not be reached due to the dependency check
        users = []
    return users


@router.get("/me/subordinates", response_model=List[User])
def read_my_subordinates(
    *,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_user),
):
    """
    Retrieve all subordinates for the current user.
    - Admins can retrieve all users.
    - Team leads and department heads can retrieve their own subordinates.
    """
    if current_user.role == UserRole.ADMIN:
        return user_crud.user.get_multi(db)

    if current_user.role not in [UserRole.TEAM_LEAD, UserRole.DEPT_HEAD]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view subordinates.",
        )
    
    subordinates = user_crud.user.get_subordinates(db, user_id=current_user.id)
    return subordinates


@router.get("/me/history", response_model=UserHistoryResponse)
def read_my_history(
    *,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
):
    """
    Retrieve own user history.
    """
    return user_crud.user.get_user_history(db, user_id=current_user.id)


@router.get("/{user_id}/history", response_model=UserHistoryResponse)
def read_user_history(
    *,
    user_id: int,
    db: Session = Depends(deps.get_db),
    user_to_view: UserModel = Depends(deps.get_user_as_subordinate),
):
    """
    Retrieve a specific user's history. (Admin or Manager of the user only)
    """
    return user_crud.user.get_user_history(db, user_id=user_to_view.id)


@router.get(
    "/{user_id}/project-weights",
    response_model=List[ProjectMemberWeightDetail],
)
def read_user_project_weights(
    *,
    db: Session = Depends(deps.get_db),
    user_to_view: UserModel = Depends(deps.get_user_as_subordinate),
):
    """
    Retrieve a specific user's project participation weights.
    (Admin or Manager of the user only)
    """
    weights = project_member_crud.project_member.get_multi_by_user_with_project_details(
        db, user_id=user_to_view.id
    )
    return weights


@router.put(
    "/{user_id}/project-weights",
    response_model=List[ProjectMemberWeightDetail],
)
def update_user_project_weights(
    *,
    weights_in: UserProjectWeightsUpdate,
    db: Session = Depends(deps.get_db),
    user_to_view: UserModel = Depends(deps.get_user_as_subordinate),
):
    """
    Update a specific user's project participation weights.
    The sum of weights must be 100.
    (Admin or Manager of the user only)
    """
    # Validate that the sum of weights is 100
    total_weight = sum(w.participation_weight for w in weights_in.weights)
    if total_weight != 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Participation weights must sum to 100.",
        )

    # Overwrite the weights in the database
    project_member_crud.project_member.overwrite_user_project_weights(
        db, user_id=user_to_view.id, weights=weights_in.weights
    )

    # Return the updated list of weights
    return project_member_crud.project_member.get_multi_by_user_with_project_details(
        db, user_id=user_to_view.id
    )