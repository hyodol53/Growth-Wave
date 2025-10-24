
from typing import Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.crud import organization as crud_org


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            full_name=obj_in.full_name,
            hashed_password=get_password_hash(obj_in.password),
            role=obj_in.role,
            organization_id=obj_in.organization_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_subordinates(self, db: Session, *, user_id: int) -> list[User]:
        user = self.get(db, id=user_id)
        if not user or not user.organization_id:
            return []

        descendant_orgs = crud_org.get_all_descendant_orgs(db, user.organization_id)
        descendant_org_ids = [org.id for org in descendant_orgs]
        
        # Include the user's own organization
        all_org_ids = descendant_org_ids + [user.organization_id]

        subordinates = (
            db.query(User)
            .filter(User.organization_id.in_(all_org_ids), User.id != user_id)
            .all()
        )
        return subordinates


user = CRUDUser(User)
