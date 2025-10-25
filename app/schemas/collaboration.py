from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from typing import List, Dict
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

    model_config = ConfigDict(from_attributes=True)


# Schemas for Network Visualization
class CollaborationNode(BaseModel):
    id: int
    label: str
    value: int = 1 # Default value for node size

class CollaborationEdge(BaseModel):
    source: int
    target: int
    value: int = 1 # Default value for edge thickness

class CollaborationGraph(BaseModel):
    nodes: List[CollaborationNode]
    edges: List[CollaborationEdge]

class CollaborationAnalysis(BaseModel):
    most_reviews: List[Dict[str, int]] = Field(default_factory=list)
    most_help: List[Dict[str, int]] = Field(default_factory=list)

class CollaborationData(BaseModel):
    graph: CollaborationGraph
    analysis: CollaborationAnalysis
