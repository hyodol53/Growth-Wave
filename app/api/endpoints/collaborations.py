from typing import List
from fastapi import APIRouter, Depends
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
