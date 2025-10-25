
from typing import Optional

from sqlalchemy.orm import Session



from app.crud.base import CRUDBase

from app.models.user import User

from app.schemas.user import UserCreate, UserUpdate, UserHistoryResponse, UserHistoryEntry, ProjectHistoryItem

from app.core.security import get_password_hash, verify_password

from app.crud import (

    organization as crud_org,

    evaluation_period as crud_eval_period,

    final_evaluation as crud_final_eval,

    project_member as crud_proj_member,

)





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

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

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

    def get_user_history(self, db: Session, *, user_id: int) -> UserHistoryResponse:
        all_periods = crud_eval_period.evaluation_period.get_multi(db, limit=1000)
        
        history_entries = []
        for period in all_periods:
            final_eval = crud_final_eval.final_evaluation.get_by_evaluatee_and_period(
                db, evaluatee_id=user_id, evaluation_period=period.name
            )
            
            project_memberships = crud_proj_member.project_member.get_multi_by_user_and_period(
                db, user_id=user_id, start_date=period.start_date, end_date=period.end_date
            )
            
            project_history = [
                ProjectHistoryItem(
                    project_name=pm.project.name,
                    participation_weight=pm.participation_weight,
                    is_pm=pm.is_pm,
                )
                for pm in project_memberships
            ]
            
            entry = UserHistoryEntry(
                evaluation_period=period.name,
                final_evaluation=final_eval,
                projects=project_history,
            )
            history_entries.append(entry)
            
        return UserHistoryResponse(history=history_entries)



    





user = CRUDUser(User)


