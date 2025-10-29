from pydantic import BaseModel, ConfigDict
from typing import Optional, List


# Shared properties
class ProjectMemberBase(BaseModel):
    user_id: int
    project_id: int
    is_pm: bool = False
    participation_weight: int

# Properties to receive on item creation
class ProjectMemberCreate(ProjectMemberBase):
    pass

# Properties to receive on item update
class ProjectMemberUpdate(BaseModel):
    participation_weight: int

# Properties shared by models stored in DB
class ProjectMemberInDBBase(ProjectMemberBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class ProjectMember(ProjectMemberInDBBase):
    pass

# Properties properties stored in DB
class ProjectMemberInDB(ProjectMemberInDBBase):
    pass


# Schema for a single project's weight
class ProjectWeight(BaseModel):
    project_id: int
    participation_weight: int

# Schema for updating a user's weights across multiple projects
class UserProjectWeightsUpdate(BaseModel):
    weights: List[ProjectWeight]

# Schema for returning a user's project weight with project name
class ProjectMemberWeightDetail(BaseModel):
    project_id: int
    project_name: str
    participation_weight: int


class ProjectMemberDetail(BaseModel):
    user_id: int
    full_name: str
    is_pm: bool
    participation_weight: int
