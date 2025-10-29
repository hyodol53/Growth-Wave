from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.schemas.project_member import (
    ProjectMember,
    ProjectMemberDetail,
    ProjectMemberAdd,
)
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
    # A dept_head can only create projects where the PM is in their own department.
    pm_user = crud_user.user.get(db, id=project_in.pm_id)
    if not pm_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project Manager with id {project_in.pm_id} not found.",
        )

    if current_user.role == "dept_head" and pm_user.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Department heads can only create projects with a PM from their own department.",
        )
    project = crud_project.project.create(db=db, obj_in=project_in)

    # Automatically add the PM as a project member
    crud_pm.project_member.add_member_with_auto_weight(
        db=db,
        user_id=project.pm_id,
        project_id=project.id,
        is_pm=True,
    )

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
    # Authorization check: Dept heads can only manage projects where the PM is in their department.
    if current_user.role == "dept_head" and project.pm.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Department heads can only manage projects where the PM is in their own department.",
        )

    # If the PM is being updated, ensure the new PM is also in the same department
    if project_in.pm_id is not None:
        new_pm_user = crud_user.user.get(db, id=project_in.pm_id)
        if not new_pm_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"New Project Manager with id {project_in.pm_id} not found.",
            )
        if current_user.role == "dept_head" and new_pm_user.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Department heads can only assign a PM from their own department.",
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
    # Authorization check: Dept heads can only manage projects where the PM is in their department.
    if current_user.role == "dept_head" and project.pm.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Department heads can only delete projects where the PM is in their own department.",
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


@router.post("/{project_id}/members", response_model=ProjectMember)
def add_project_member(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    member_in: ProjectMemberAdd,
    current_user: UserModel = Depends(deps.get_current_dept_head_user),
) -> Any:
    """
    Add a member to a project. (Dept Head or Admin only)
    """
    project = crud_project.project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    user_to_add = crud_user.user.get(db=db, id=member_in.user_id)
    if not user_to_add:
        raise HTTPException(status_code=404, detail="User to add not found")

    # Authorization for Dept Head
    if current_user.role == "dept_head":
        if project.pm.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=403,
                detail="Dept heads can only add members to projects managed by their department.",
            )
        if user_to_add.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=403,
                detail="Dept heads can only add members from their own department.",
            )

    # Check if member already exists
    existing_member = crud_pm.project_member.get_by_user_and_project(
        db=db, user_id=member_in.user_id, project_id=project_id
    )
    if existing_member:
        raise HTTPException(
            status_code=409, detail="User is already a member of this project"
        )

    new_member = crud_pm.project_member.add_member_with_auto_weight(
        db=db,
        user_id=member_in.user_id,
        project_id=project_id,
        is_pm=member_in.is_pm,
    )
    return new_member
