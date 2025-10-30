from pydantic import BaseModel
from datetime import date
from typing import Optional

# Shared properties
class ProjectBase(BaseModel):
    name: str
    pm_id: Optional[int] = None
    evaluation_period_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None

# Properties to receive on item creation
class ProjectCreate(ProjectBase):
    name: str
    pm_id: int
    evaluation_period_id: int

# Properties to receive on item update
class ProjectUpdate(ProjectBase):
    pass

# Properties shared by models stored in DB
class ProjectInDBBase(ProjectBase):
    id: int
    name: str
    pm_id: int
    evaluation_period_id: int

    class Config:
        from_attributes = True

# Properties to return to client
class Project(ProjectInDBBase):
    pass

# Properties properties stored in DB
class ProjectInDB(ProjectInDBBase):
    pass
