from typing import List, Optional
from datetime import date

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project_member import ProjectMember
from app.models.project import Project
from app.models.user import User
from app.models.evaluation import EvaluationPeriod
from app.schemas.project_member import (
    ProjectMemberCreate,
    ProjectMemberUpdate,
    ProjectWeight,
)


class CRUDProjectMember(
    CRUDBase[ProjectMember, ProjectMemberCreate, ProjectMemberUpdate]
):
    def get_by_user_and_project(
        self, db: Session, *, user_id: int, project_id: int
    ) -> Optional[ProjectMember]:
        return (
            db.query(ProjectMember)
            .filter(
                ProjectMember.user_id == user_id, ProjectMember.project_id == project_id
            )
            .first()
        )

    def get_multi_by_user(self, db: Session, *, user_id: int) -> List[ProjectMember]:
        return db.query(ProjectMember).filter(ProjectMember.user_id == user_id).all()

    def get_multi_by_user_and_period(self, db: Session, *, user_id: int, start_date: date, end_date: date) -> List[ProjectMember]:
        return (
            db.query(self.model)
            .join(Project)
            .filter(
                ProjectMember.user_id == user_id,
                Project.start_date <= end_date,
                Project.end_date >= start_date,
            )
            .all()
        )

    def get_multi_by_user_and_evaluation_period(self, db: Session, *, user_id: int, evaluation_period_id: int) -> List[ProjectMember]:
        return (
            db.query(self.model)
            .join(Project)
            .filter(
                ProjectMember.user_id == user_id,
                Project.evaluation_period_id == evaluation_period_id,
            )
            .all()
        )

    def get_multi_by_user_and_period_id(
        self, db: Session, *, user_id: int, period_id: int
    ) -> List[ProjectMember]:
        period = db.query(EvaluationPeriod).filter(EvaluationPeriod.id == period_id).first()
        if not period:
            return []
        return self.get_multi_by_user_and_period(
            db, user_id=user_id, start_date=period.start_date, end_date=period.end_date
        )

    def get_multi_by_project_with_user_details(
        self, db: Session, *, project_id: int
    ) -> list:
        return (
            db.query(
                ProjectMember.user_id.label("user_id"),
                User.full_name.label("full_name"),
                ProjectMember.is_pm.label("is_pm"),
                ProjectMember.participation_weight.label("participation_weight"),
            )
            .join(User, ProjectMember.user_id == User.id)
            .filter(ProjectMember.project_id == project_id)
            .all()
        )

    def get_multi_by_user_with_project_details(
        self, db: Session, *, user_id: int
    ) -> list:
        """
        Fetches all project memberships for a user, including project names.
        """
        return (
            db.query(
                Project.id.label("project_id"),
                Project.name.label("project_name"),
                ProjectMember.participation_weight.label("participation_weight"),
            )
            .join(Project, ProjectMember.project_id == Project.id)
            .filter(ProjectMember.user_id == user_id)
            .all()
        )

    def overwrite_user_project_weights(
        self, db: Session, *, user_id: int, weights: List[ProjectWeight]
    ) -> List[ProjectMember]:
        """
        Updates participation weights for a user's existing project memberships.
        This function does not create or delete memberships, only updates weights.
        """
        # Fetch existing memberships in a dictionary for quick access
        existing_memberships = {
            m.project_id: m
            for m in self.get_multi_by_user(db=db, user_id=user_id)
        }

        updated_memberships = []
        for weight_info in weights:
            membership = existing_memberships.get(weight_info.project_id)
            if membership:
                membership.participation_weight = weight_info.participation_weight
                db.add(membership)
                updated_memberships.append(membership)

        db.commit()
        return updated_memberships

    def add_member_with_auto_weight(
        self, db: Session, *, user_id: int, project_id: int, is_pm: bool
    ) -> ProjectMember:
        # Calculate current total weight for the user
        current_memberships = self.get_multi_by_user(db=db, user_id=user_id)
        total_weight = sum(m.participation_weight for m in current_memberships)

        # New weight is the remaining percentage, with a floor of 0
        new_weight = max(0, 100 - total_weight)

        # Create the new project member record
        create_schema = ProjectMemberCreate(
            user_id=user_id,
            project_id=project_id,
            is_pm=is_pm,
            participation_weight=new_weight,
        )
        return self.create(db=db, obj_in=create_schema)


project_member = CRUDProjectMember(ProjectMember)
