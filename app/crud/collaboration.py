from app.crud.base import CRUDBase
from app.models.collaboration import CollaborationInteraction
from app.schemas.collaboration import CollaborationInteractionCreate


class CRUDCollaborationInteraction(CRUDBase[CollaborationInteraction, CollaborationInteractionCreate, None]):
    pass


collaboration_interaction = CRUDCollaborationInteraction(CollaborationInteraction)
