
from typing import List, Dict, Any

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel
from app.schemas.organization import Organization, OrganizationCreate, OrganizationUpdate
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
