from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.collectors.jira_collector import JiraCollector
from app.collectors.bitbucket_collector import BitbucketCollector

router = APIRouter()

@router.get("/network-data", response_model=schemas.CollaborationData)
def get_collaboration_network_data(
    *,
    db: Session = Depends(deps.get_db),
    project_id: Optional[int] = None,
    organization_id: Optional[int] = None,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve collaboration network data, filtered by project or organization.
    """
    if not project_id and not organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either project_id or organization_id must be provided.",
        )
    
    data = crud.collaboration.collaboration_interaction.get_collaboration_data(
        db=db, project_id=project_id, organization_id=organization_id
    )
    return data

@router.post("/collect", status_code=status.HTTP_202_ACCEPTED)
def collect_collaboration_data(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Trigger the collection of collaboration data from all linked external accounts.
    (Admin only)
    """
    total_new_interactions = 0
    users = crud.user.get_multi(db, skip=0, limit=1000) # Get all users

    for user in users:
        accounts = crud.external_account.get_multi_by_owner(db, owner_id=user.id)
        for account in accounts:
            collector = None
            if account.provider == models.external_account.Provider.JIRA:
                collector = JiraCollector(db, account.provider)
            elif account.provider == models.external_account.Provider.BITBUCKET:
                collector = BitbucketCollector(db, account.provider)
            
            if collector:
                try:
                    new_interactions = collector.collect(user=user, account=account)
                    total_new_interactions += new_interactions
                except Exception as e:
                    # In a real app, you'd want more robust error logging here
                    print(f"ERROR: Failed to collect data for user {user.id} and account {account.id}. Reason: {e}")

    return {"message": "Collection process started.", "total_new_interactions": total_new_interactions}