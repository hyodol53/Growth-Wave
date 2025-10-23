
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.models.user import UserRole

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

    class Config:
        orm_mode = True

# Schema for updating user data
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    organization_id: Optional[int] = None
    role: Optional[UserRole] = None
