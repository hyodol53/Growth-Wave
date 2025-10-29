from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.project import Project
from app.models.user import User, UserRole
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.crud import user as crud_user

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Project]:
        return db.query(Project).filter(Project.name == name).first()

    def get_multi_for_user(self, db: Session, *, user: User) -> List[Project]:
        if user.role == UserRole.ADMIN:
            return self.get_multi(db)
        
        if user.role == UserRole.DEPT_HEAD:
            subordinate_ids = {sub.id for sub in crud_user.user.get_subordinates(db, user_id=user.id)}
            # Also include projects where the user themself is the PM
            subordinate_ids.add(user.id)
            
            return db.query(self.model).filter(self.model.pm_id.in_(subordinate_ids)).all()
        
        # Team leads and employees should not see any projects via this generic endpoint
        return []


project = CRUDProject(Project)

