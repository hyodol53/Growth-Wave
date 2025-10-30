from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from typing import List, Dict, Any
from app.models.collaboration import InteractionType, CollaborationCategory

class CollaborationInteractionBase(BaseModel):
    source_user_id: int
    target_user_id: int
    project_id: int
    interaction_type: InteractionType
    category: CollaborationCategory
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
    most_support: List[Dict[str, Any]] = Field(default_factory=list)
    most_requests: List[Dict[str, Any]] = Field(default_factory=list)

class CollaborationData(BaseModel):
    graph: CollaborationGraph
    analysis: CollaborationAnalysis
