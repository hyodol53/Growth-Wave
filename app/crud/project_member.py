from typing import List, Optional
from datetime import date

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project_member import ProjectMember
from app.models.project import Project
from app.schemas.project_member import ProjectMemberCreate, ProjectMemberUpdate

class CRUDProjectMember(CRUDBase[ProjectMember, ProjectMemberCreate, ProjectMemberUpdate]):
    def get_by_user_and_project(
        self, db: Session, *, user_id: int, project_id: int
    ) -> Optional[ProjectMember]:
        return (
            db.query(ProjectMember)
            .filter(ProjectMember.user_id == user_id, ProjectMember.project_id == project_id)
            .first()
        )

    def get_multi_by_user(self, db: Session, *, user_id: int) -> List[ProjectMember]:
        return db.query(ProjectMember).filter(ProjectMember.user_id == user_id).all()

    def get_multi_by_user_and_period(
        self, db: Session, *, user_id: int, start_date: date, end_date: date
    ) -> List[ProjectMember]:
        return (
            db.query(ProjectMember)
            .join(Project)
            .filter(
                ProjectMember.user_id == user_id,
                Project.start_date <= end_date,
                Project.end_date >= start_date,
            )
            .all()
        )

project_member = CRUDProjectMember(ProjectMember)
