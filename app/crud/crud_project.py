from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User, UserRole
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.crud import user as crud_user

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Project]:
        return db.query(Project).filter(Project.name == name).first()

    def get_multi_by_filter(
        self, 
        db: Session, 
        *, 
        evaluation_period_id: Optional[int] = None,
        pm_id: Optional[int] = None,
        user_id: Optional[int] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Project]:
        query = db.query(self.model)

        if evaluation_period_id is not None:
            query = query.filter(Project.evaluation_period_id == evaluation_period_id)
        
        if pm_id is not None:
            query = query.filter(Project.pm_id == pm_id)

        if user_id is not None:
            query = query.join(ProjectMember).filter(ProjectMember.user_id == user_id)

        return query.offset(skip).limit(limit).all()


project = CRUDProject(Project)
