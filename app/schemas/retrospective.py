from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Properties to receive on item creation
class RetrospectiveCreate(BaseModel):
    title: str
    content: str
    evaluation_period_id: Optional[int] = None

# Properties to receive on item update
class RetrospectiveUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Properties shared by models stored in DB
class RetrospectiveInDBBase(BaseModel):
    id: int
    user_id: int
    title: str
    content: Optional[str] = None
    evaluation_period_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Properties to return to client
class Retrospective(RetrospectiveInDBBase):
    pass