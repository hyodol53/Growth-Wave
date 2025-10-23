from pydantic import BaseModel
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
class ProjectUpdate(ProjectBase):
    pass

# Properties shared by models stored in DB
class ProjectInDBBase(ProjectBase):
    id: int

    class Config:
        orm_mode = True

# Properties to return to client
class Project(ProjectInDBBase):
    pass

# Properties properties stored in DB
class ProjectInDB(ProjectInDBBase):
    pass
