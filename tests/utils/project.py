from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from app import models
from app.schemas.project import ProjectCreate
from app.schemas.project_member import ProjectMemberCreate
from app.crud import crud_project, project_member as crud_pm
from tests.utils.common import random_lower_string
from tests.utils.evaluation_period import create_random_evaluation_period


def create_random_project(
    db: Session,
    *,
    pm_id: int,
    evaluation_period_id: Optional[int] = None,
    name: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> models.Project:
    if evaluation_period_id is None:
        eval_period = create_random_evaluation_period(db)
        evaluation_period_id = eval_period.id
        
    if name is None:
        name = random_lower_string()
    if start_date is None:
        start_date = date(2025, 1, 1)
    if end_date is None:
        end_date = date(2025, 6, 30)

    project_in = ProjectCreate(
        name=name,
        pm_id=pm_id,
        evaluation_period_id=evaluation_period_id,
        start_date=start_date,
        end_date=end_date
    )
    return crud_project.project.create(db=db, obj_in=project_in)

def add_user_to_project(db: Session, *, user_id: int, project_id: int, is_pm: bool = False, participation_weight: int = 100) -> models.ProjectMember:
    project_member_in = ProjectMemberCreate(user_id=user_id, project_id=project_id, is_pm=is_pm, participation_weight=participation_weight)
    return crud_pm.project_member.create(db=db, obj_in=project_member_in)