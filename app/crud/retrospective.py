from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.retrospective import Retrospective
from app.schemas.retrospective import RetrospectiveCreate, RetrospectiveUpdate

class CRUDRetrospective(CRUDBase[Retrospective, RetrospectiveCreate, RetrospectiveUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: RetrospectiveCreate, user_id: int
    ) -> Retrospective:
        db_obj = self.model(**obj_in.model_dump(), user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Retrospective]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_owner(
        self, db: Session, *, id: int, user_id: int
    ) -> Optional[Retrospective]:
        return (
            db.query(self.model)
            .filter(self.model.id == id, self.model.user_id == user_id)
            .first()
        )

    def remove_by_owner(self, db: Session, *, id: int, user_id: int) -> Optional[Retrospective]:
        obj = self.get_by_owner(db=db, id=id, user_id=user_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

retrospective = CRUDRetrospective(Retrospective)
