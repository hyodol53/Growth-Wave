from sqlalchemy.orm import Session
from app import crud, models
from app.schemas.project import ProjectCreate
from tests.utils.utils import random_lower_string
from tests.utils.organization import create_random_organization
from typing import Optional

def create_random_project(db: Session, *, owner_org_id: int, name: Optional[str] = None) -> models.Project:
    if name is None:
        name = random_lower_string()
    project_in = ProjectCreate(name=name, owner_org_id=owner_org_id)
    return crud.project.project.create(db=db, obj_in=project_in)
