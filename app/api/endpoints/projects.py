from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.schemas.project_member import ProjectMember, ProjectMemberDetail
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
