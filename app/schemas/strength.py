from pydantic import BaseModel
from typing import List

# Schema for returning a single strength with its received count
class StrengthStat(BaseModel):
    hashtag: str
    count: int

# Schema for a user's public strength profile
class StrengthProfile(BaseModel):
    user_id: int
    full_name: str
    strengths: List[StrengthStat] = []
