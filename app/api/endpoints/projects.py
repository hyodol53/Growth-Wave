from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel
from app.schemas.project_member import ProjectMember, ProjectMemberWeightsUpdate
from app.crud import project_member as crud_pm
from app.crud import user as crud_user
from app.api import deps

router = APIRouter()

@router.post("/members/weights", response_model=List[ProjectMember])
def set_project_member_weights(
    *, 
    db: Session = Depends(get_db), 
    weights_in: ProjectMemberWeightsUpdate, 
    current_user: UserModel = Depends(deps.get_current_dept_head_user)
):
    """
    Set participation weights for a user in multiple projects. (Dept Head only)

    - The user must belong to the department of the dept head.
    - The sum of weights must be exactly 100.
    """
    target_user = crud_user.user.get(db, id=weights_in.user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")

    # Authorization: Dept head can only manage users in their own department.
    # Note: A dept head's organization_id points to the '실'.
    if target_user.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only set weights for users in your own department"
        )

    # Validation: Sum of weights must be 100
    total_weight = sum(w.participation_weight for w in weights_in.weights)
    if total_weight != 100:
        raise HTTPException(
            status_code=400, 
            detail=f"Total participation weight must be 100, but it is {total_weight}"
        )

    # Clear existing weights to ensure a clean slate
    existing_memberships = crud_pm.project_member.get_multi_by_user(db, user_id=target_user.id)
    for membership in existing_memberships:
        db.delete(membership)
    db.commit()

    # Create new weight entries
    created_memberships = []
    for weight in weights_in.weights:
        membership = crud_pm.project_member.create(db, obj_in={
            "user_id": target_user.id,
            "project_id": weight.project_id,
            "participation_weight": weight.participation_weight
        })
        created_memberships.append(membership)
    
    return created_memberships
