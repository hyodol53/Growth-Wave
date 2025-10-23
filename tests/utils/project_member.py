from sqlalchemy.orm import Session
from app import crud
from app.models.project_member import ProjectMember
from app.schemas.project_member import ProjectMemberCreate

def create_project_member(
    db: Session, *, project_id: int, user_id: int, is_pm: bool = False, participation_weight: int = 100
) -> ProjectMember:
    project_member_in = ProjectMemberCreate(
        project_id=project_id, user_id=user_id, is_pm=is_pm, participation_weight=participation_weight
    )
    return crud.project_member.project_member.create(db=db, obj_in=project_member_in)
