
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List

from app.models.user import UserRole
from app.schemas.evaluation import FinalEvaluation
from app.schemas.project_member import ProjectMember


# Base schema for user properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

# Schema for user creation
class UserCreate(UserBase):
    username: str
    password: str
    role: UserRole = UserRole.EMPLOYEE
    organization_id: Optional[int] = None

# Schema for reading user data
class User(UserBase):
    id: int
    username: str
    role: UserRole
    organization_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# Schema for updating user data
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    organization_id: Optional[int] = None
    role: Optional[UserRole] = None


# Schemas for User History
class ProjectHistoryItem(BaseModel):
    project_name: str
    participation_weight: int
    is_pm: bool

    model_config = ConfigDict(from_attributes=True)


class UserHistoryEntry(BaseModel):
    evaluation_period: str
    final_evaluation: Optional[FinalEvaluation] = None
    projects: List[ProjectHistoryItem] = []


class UserHistoryResponse(BaseModel):
    history: List[UserHistoryEntry]
