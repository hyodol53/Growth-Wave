from sqlalchemy.orm import Session
from datetime import datetime

from app import crud
from app.models.user import User
from app.models.project import Project
from app.models.collaboration import InteractionType
from app.schemas.collaboration import CollaborationInteractionCreate

def create_random_interaction(db: Session, source_user: User, target_user: User, project: Project, type: InteractionType) -> None:
    interaction_in = CollaborationInteractionCreate(
        source_user_id=source_user.id,
        target_user_id=target_user.id,
        project_id=project.id,
        interaction_type=type,
        occurred_at=datetime.utcnow()
    )
    crud.collaboration.collaboration_interaction.create(db, obj_in=interaction_in)
