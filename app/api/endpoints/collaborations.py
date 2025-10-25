from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.api import deps

router = APIRouter()

@router.post("/collect", response_model=List[schemas.CollaborationInteraction])
def collect_collaboration_data(
    *,
    db: Session = Depends(deps.get_db),
    interactions_in: List[schemas.CollaborationInteractionCreate],
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    """
    Collect collaboration data from external systems.
    (This is a mock endpoint for now. In a real scenario, this would be triggered by a background worker)
    """
    interactions = []
    for interaction_in in interactions_in:
        interaction = crud.collaboration.collaboration_interaction.create(db, obj_in=interaction_in)
        interactions.append(interaction)
    return interactions

@router.get("/network-data", response_model=schemas.CollaborationData)
def get_collaboration_network_data(
    db: Session = Depends(deps.get_db),
    project_id: Optional[int] = None,
    organization_id: Optional[int] = None,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Get collaboration network data for visualization, optionally filtered by project or organization.
    """
    if not project_id and not organization_id:
        raise HTTPException(
            status_code=400,
            detail="Either project_id or organization_id must be provided.",
        )
    
    data = crud.collaboration.collaboration_interaction.get_collaboration_data(
        db, project_id=project_id, organization_id=organization_id
    )
    return data
