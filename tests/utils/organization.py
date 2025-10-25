from sqlalchemy.orm import Session
from app import crud, models
from app.schemas.organization import OrganizationCreate
from tests.utils.utils import random_lower_string
from typing import Optional

def create_random_organization(
    db: Session, 
    *, 
    name: Optional[str] = None,
    level: int = 1,
    parent_id: Optional[int] = None, 
    department_grade: Optional[str] = None
) -> models.Organization:
    if name is None:
        name = random_lower_string()
    organization_in = OrganizationCreate(name=name, level=level, parent_id=parent_id, department_grade=department_grade)
    return crud.organization.create_organization(db=db, org=organization_in)
