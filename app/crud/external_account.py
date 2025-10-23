from sqlalchemy.orm import Session
from app.models.external_account import ExternalAccount
from app.schemas.external_account import ExternalAccountCreate
from app.core.security import fernet

def create_external_account(db: Session, *, owner_id: int, obj_in: ExternalAccountCreate) -> ExternalAccount:
    encrypted_token = fernet.encrypt(obj_in.access_token.encode())
    db_obj = ExternalAccount(
        owner_id=owner_id,
        account_type=obj_in.account_type,
        username=obj_in.username,
        encrypted_access_token=encrypted_token.decode()
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_external_accounts_by_owner(db: Session, *, owner_id: int) -> list[ExternalAccount]:
    return db.query(ExternalAccount).filter(ExternalAccount.owner_id == owner_id).all()

def get_external_account(db: Session, *, account_id: int) -> ExternalAccount | None:
    return db.query(ExternalAccount).filter(ExternalAccount.id == account_id).first()

def delete_external_account(db: Session, *, account_id: int):
    db_obj = db.query(ExternalAccount).filter(ExternalAccount.id == account_id).first()
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj