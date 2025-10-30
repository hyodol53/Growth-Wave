from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# Schema for creating a new praise
class PraiseCreate(BaseModel):
    recipient_id: int
    message: str = Field(..., min_length=1, max_length=500)
    hashtag: str = Field(..., min_length=1, max_length=100)

# Schema for representing a praise in the inbox API response
class Praise(BaseModel):
    sender_display_name: str # e.g., "익명의 고라니"
    message: str
    hashtag: str
    received_at: datetime = Field(..., alias="created_at")

    model_config = ConfigDict(from_attributes=True)
