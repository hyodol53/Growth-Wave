from sqlalchemy.orm import Session

from app import crud
from app.schemas.external_account import ExternalAccountCreate
from app.models.external_account import AccountType
from app.core.security import fernet


def create_random_external_account(
    db: Session, *, owner_id: int, account_type: AccountType = AccountType.JIRA
) -> None:
    account_in = ExternalAccountCreate(
        account_type=account_type,
        username=f"testuser@{account_type.value}.com",
        access_token=f"test-token-for-{owner_id}",
    )
    crud.external_account.create_external_account(db=db, owner_id=owner_id, obj_in=account_in)
