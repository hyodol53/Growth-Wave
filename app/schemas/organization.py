
from pydantic import BaseModel
from typing import Optional, List

# Forward declaration for recursive schema
class Organization(BaseModel):
    id: int
    name: str
    level: int
    department_grade: Optional[str] = None
    parent_id: Optional[int] = None
    children: List["Organization"] = []

    class Config:
        orm_mode = True

# Update forward reference
Organization.update_forward_refs()

class OrganizationCreate(BaseModel):
    name: str
    level: int
    parent_id: Optional[int] = None
    department_grade: Optional[str] = None
