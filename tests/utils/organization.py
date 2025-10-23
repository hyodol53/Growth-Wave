from sqlalchemy.orm import Session
from app import crud, models
from app.schemas.organization import OrganizationCreate
from tests.utils.utils import random_lower_string

def create_random_organization(db: Session) -> models.Organization:
    name = random_lower_string()
    organization_in = OrganizationCreate(name=name, level=1)
    return crud.organization.create_organization(db=db, org=organization_in)
