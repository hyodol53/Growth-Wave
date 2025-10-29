from sqlalchemy.orm import Session
from app import crud, models
from app.schemas.project import ProjectCreate
from tests.utils.utils import random_lower_string
from tests.utils.organization import create_random_organization
from typing import Optional
from datetime import date

def create_random_project(
    db: Session, 
    *, 
    pm_id: int, 
    name: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> models.Project:
    if name is None:
        name = random_lower_string()
    project_in = ProjectCreate(
        name=name, 
        pm_id=pm_id, 
        start_date=start_date, 
        end_date=end_date
    )
    return crud.project.project.create(db=db, obj_in=project_in)
