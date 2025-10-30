from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("", response_model=schemas.ExternalAccount, status_code=status.HTTP_201_CREATED)
def create_external_account(
    *,
    db: Session = Depends(deps.get_db),
    account_in: schemas.ExternalAccountCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Link a new external account for the current user.
    """
    # Optional: Check if an account with the same provider and account_id already exists for this user
    # This logic can be added in the CRUD layer if needed.
    account = crud.external_account.create_with_owner(
        db=db, obj_in=account_in, owner_id=current_user.id
    )
    return account

@router.get("", response_model=List[schemas.ExternalAccount])
def read_external_accounts(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve external accounts for the current user.
    """
    accounts = crud.external_account.get_multi_by_owner(db=db, owner_id=current_user.id)
    return accounts

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_external_account(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> None:
    """
    Delete an external account.
    """
    account = crud.external_account.get(db=db, id=id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    if account.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    crud.external_account.remove(db=db, id=id)
    return None
