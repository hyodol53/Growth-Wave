from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Project]:
        return db.query(Project).filter(Project.name == name).first()

project = CRUDProject(Project)
