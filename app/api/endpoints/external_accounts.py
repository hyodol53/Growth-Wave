from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.ExternalAccount, status_code=201)
def create_external_account(
    *,
    db: Session = Depends(deps.get_db),
    account_in: schemas.ExternalAccountCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Create new external account for the current user.
    """
    account = crud.external_account.create_external_account(
        db=db, owner_id=current_user.id, obj_in=account_in
    )
    return account

@router.get("/", response_model=list[schemas.ExternalAccount])
def read_external_accounts(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Retrieve external accounts for the current user.
    """
    accounts = crud.external_account.get_external_accounts_by_owner(
        db=db, owner_id=current_user.id
    )
    return accounts

@router.delete("/{account_id}", response_model=schemas.ExternalAccount)
def delete_external_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Delete an external account.
    """
    account = crud.external_account.get_external_account(db=db, account_id=account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    deleted_account = crud.external_account.delete_external_account(db=db, account_id=account_id)
    return deleted_account