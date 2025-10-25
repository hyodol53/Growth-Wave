
from pydantic import BaseModel, ConfigDict
from typing import Optional, List


# Forward declaration for recursive schema
class Organization(BaseModel):
    id: int
    name: str
    level: int
    department_grade: Optional[str] = None
    parent_id: Optional[int] = None
    children: List["Organization"] = []

    model_config = ConfigDict(from_attributes=True)

# Update forward reference
Organization.model_rebuild()

class OrganizationCreate(BaseModel):
    name: str

    level: int
    parent_id: Optional[int] = None
    department_grade: Optional[str] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    parent_id: Optional[int] = None
    department_grade: Optional[str] = None
