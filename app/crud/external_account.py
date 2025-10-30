from sqlalchemy.orm import Session
from typing import List

from app.crud.base import CRUDBase
from app.models.external_account import ExternalAccount
from app.schemas.external_account import ExternalAccountCreate
from app.core.security import encrypt_data

class CRUDExternalAccount(CRUDBase[ExternalAccount, ExternalAccountCreate, None]):
    def create_with_owner(
        self, db: Session, *, obj_in: ExternalAccountCreate, owner_id: int
    ) -> ExternalAccount:
        
        encrypted_credentials = encrypt_data(obj_in.credentials)
        
        db_obj = self.model(
            provider=obj_in.provider,
            account_id=obj_in.account_id,
            encrypted_credentials=encrypted_credentials,
            owner_id=owner_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[ExternalAccount]:
        return (
            db.query(self.model)
            .filter(ExternalAccount.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

external_account = CRUDExternalAccount(ExternalAccount)
