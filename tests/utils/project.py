from sqlalchemy.orm import Session
from app import crud, models
from app.schemas.project import ProjectCreate
from tests.utils.utils import random_lower_string
from tests.utils.organization import create_random_organization

def create_random_project(db: Session) -> models.Project:
    name = random_lower_string()
    organization = create_random_organization(db)
    project_in = ProjectCreate(name=name, owner_org_id=organization.id)
    return crud.project.project.create(db=db, obj_in=project_in)
