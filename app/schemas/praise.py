from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List

# Schema for representing a strength hashtag within a praise response
class StrengthInPraise(BaseModel):
    hashtag: str
    model_config = ConfigDict(from_attributes=True)

# Schema for creating a new praise
class PraiseCreate(BaseModel):
    recipient_id: int
    message: str = Field(..., min_length=1, max_length=500)
    # Users will submit a list of simple string hashtags
    hashtags: List[str] = Field(..., min_length=1, max_length=5)

# Schema for representing a praise in the database (and in API responses)
class Praise(BaseModel):
    id: int
    anonymous_name: str
    message: str
    created_at: datetime
    strengths: List[StrengthInPraise] = []

    model_config = ConfigDict(from_attributes=True)
