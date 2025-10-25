from sqlalchemy.orm import Session
from app import crud, models
from app.schemas.organization import OrganizationCreate
from tests.utils.utils import random_lower_string

def create_random_organization(db: Session, *, parent_id: int | None = None, department_grade: str | None = None) -> models.Organization:
    name = random_lower_string()
    organization_in = OrganizationCreate(name=name, level=1, parent_id=parent_id, department_grade=department_grade)
    return crud.organization.create_organization(db=db, org=organization_in)
