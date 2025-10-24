from pydantic import BaseModel
from datetime import datetime
from app.models.collaboration import InteractionType

class CollaborationInteractionBase(BaseModel):
    source_user_id: int
    target_user_id: int
    project_id: int
    interaction_type: InteractionType
    occurred_at: datetime

class CollaborationInteractionCreate(CollaborationInteractionBase):
    pass

class CollaborationInteraction(CollaborationInteractionBase):
    id: int

    class Config:
        from_attributes = True
