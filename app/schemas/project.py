from pydantic import BaseModel, ConfigDict
from typing import Optional, List


# Shared properties
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    owner_org_id: int

# Properties to receive on item creation
class ProjectCreate(ProjectBase):
    pass

# Properties to receive on item update
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_org_id: Optional[int] = None


# Properties shared by models stored in DB
class ProjectInDBBase(ProjectBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Project(ProjectInDBBase):
    pass

# Properties properties stored in DB
class ProjectInDB(ProjectInDBBase):
    pass
