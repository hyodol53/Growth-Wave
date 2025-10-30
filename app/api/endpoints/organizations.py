
from typing import List, Dict, Any

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel
from app.schemas.organization import Organization, OrganizationCreate, OrganizationUpdate, OrganizationGradeUpdate
from app.crud import organization as org_crud
from app.api import deps


router = APIRouter()

@router.post("/", response_model=Organization, status_code=201)
def create_organization(
    *, 
    db: Session = Depends(get_db), 
    org_in: OrganizationCreate, 
    current_user: UserModel = Depends(deps.get_current_admin_user)
):
    """
    Create new organization. (Admin only)
    """
    return org_crud.create_organization(db, org=org_in)

@router.get("/", response_model=List[Organization])
def read_organizations(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_user)
):
    """
    Retrieve all organizations.
    """
    return org_crud.get_organizations(db)

@router.post("/upload", response_model=Dict[str, Any])
def upload_organizations(
    *,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    current_user: UserModel = Depends(deps.get_current_admin_user)
):
    """
    Upload a file (JSON or CSV) to sync organizations. (Admin only)
    - The file should contain a list of organization data.
    - It will create, update, or delete organizations based on the file content.
    """
    if not file.filename.endswith((".json", ".csv")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only JSON or CSV are supported.")

    try:
        result = org_crud.sync_organizations_from_file(db, file=file)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process file: {e}")

@router.post("/sync-chart", response_model=Dict[str, Any])
def sync_org_chart(
    *,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    current_user: UserModel = Depends(deps.get_current_admin_user)
):
    """
    Upload a JSON file to sync the entire organization chart, including users.
    - Creates/updates organizations and users.
    - Assigns roles based on hierarchy.
    """
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only JSON is supported.")

    try:
        result = org_crud.sync_organizations_and_users_from_json(db, file=file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


@router.put("/{org_id}", response_model=Organization)
def update_organization(
    *,
    db: Session = Depends(get_db),
    org_id: int,
    org_in: OrganizationUpdate,
    current_user: UserModel = Depends(deps.get_current_admin_user)
):
    """
    Update an organization. (Admin only)
    """
    db_org = org_crud.get_organization(db, org_id=org_id)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org_crud.update_organization(db, db_org=db_org, org_in=org_in)


@router.put("/{org_id}/grade", response_model=Organization)
def set_organization_grade(
    *,
    db: Session = Depends(get_db),
    org_id: int,
    org_in: OrganizationGradeUpdate,
    current_user: UserModel = Depends(deps.get_current_center_head_or_admin_user)
):
    """
    Set the grade for a department and sync it to the department head.
    (Center Head or Admin only)
    """
    db_org = org_crud.get_organization(db, org_id=org_id)
    if not db_org:
        raise HTTPException(status_code=404, detail=f"Organization with id {org_id} not found.")

    valid_grades = ["S", "A", "B"]
    if org_in.department_grade not in valid_grades:
        raise HTTPException(status_code=400, detail=f"Invalid grade provided. Must be one of {valid_grades}.")

    return org_crud.set_department_grade(db, db_org=db_org, grade=org_in.department_grade)


@router.delete("/{org_id}", response_model=Organization)
def delete_organization(
    *,
    db: Session = Depends(get_db),
    org_id: int,
    current_user: UserModel = Depends(deps.get_current_admin_user)
):
    """
    Delete an organization. (Admin only)
    """
    db_org = org_crud.get_organization(db, org_id=org_id)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org_crud.delete_organization(db, org_id=org_id)
