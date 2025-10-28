from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.schemas.project_member import ProjectMember, ProjectMemberWeightsUpdate, ProjectMemberDetail
from app.crud import project as crud_project
from app.crud import project_member as crud_pm
from app.crud import user as crud_user
from app.api import deps

router = APIRouter()

@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: ProjectCreate,
    current_user: UserModel = Depends(deps.get_current_dept_head_user),
) -> Any:
    """
    Create new project. (Dept Head or Admin only)
    """
    # A dept_head can only create a project within their own department
    if current_user.role == "dept_head" and project_in.owner_org_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Department heads can only create projects for their own department.",
        )
    project = crud_project.project.create(db=db, obj_in=project_in)
    return project

@router.get("/", response_model=List[Project])
def read_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve projects.
    """
    projects = crud_project.project.get_multi(db, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=Project)
def read_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: UserModel = Depends(deps.get_current_user),
) -> Any:
    """
    Get project by ID.
    """
    project = crud_project.project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=Project)
def update_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    project_in: ProjectUpdate,
    current_user: UserModel = Depends(deps.get_current_dept_head_user),
) -> Any:
    """
    Update a project. (Dept Head or Admin only)
    """
    project = crud_project.project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    # Authorization check
    if current_user.role == "dept_head" and project.owner_org_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Department heads can only update projects in their own department.",
        )
    project = crud_project.project.update(db=db, db_obj=project, obj_in=project_in)
    return project

@router.delete("/{project_id}", response_model=Project)
def delete_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: UserModel = Depends(deps.get_current_dept_head_user),
) -> Any:
    """
    Delete a project. (Dept Head or Admin only)
    """
    project = crud_project.project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    # Authorization check
    if current_user.role == "dept_head" and project.owner_org_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Department heads can only delete projects in their own department.",
        )
    project = crud_project.project.remove(db=db, id=project_id)
    return project



@router.get("/{project_id}/members", response_model=List[ProjectMemberDetail])
def read_project_members(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: UserModel = Depends(deps.get_current_user),
) -> Any:
    """
    Get all members of a specific project.
    """
    project = crud_project.project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    members_data = crud_pm.project_member.get_multi_by_project_with_user_details(
        db=db, project_id=project_id
    )
    
    members = [
        ProjectMemberDetail(
            user_id=member.user_id,
            full_name=member.full_name,
            is_pm=member.is_pm,
            participation_weight=member.participation_weight,
        )
        for member in members_data
    ]
    return members


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
