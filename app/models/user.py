
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class UserRole(str, enum.Enum):
    EMPLOYEE = "employee"
    TEAM_LEAD = "team_lead"
    DEPT_HEAD = "dept_head"  # 실장
    CENTER_HEAD = "center_head" # 센터장/연구소장
    ADMIN = "admin" # 인사관리자

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    title = Column(String, nullable=True)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.EMPLOYEE, nullable=False)

    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="members")
    
    # Self-referential relationship for reporting structure
    reports_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    manager = relationship("User", remote_side=[id], back_populates="subordinates")
    subordinates = relationship("User", back_populates="manager")

    external_accounts = relationship("ExternalAccount", back_populates="owner", cascade="all, delete-orphan")

    # Project memberships for this user
    project_memberships = relationship("ProjectMember", back_populates="user", cascade="all, delete-orphan")

    # Projects managed by this user (as PM)
    projects_managed = relationship("Project", back_populates="pm", foreign_keys="[Project.pm_id]")

    # Praises received by this user
    praises_received = relationship(
        "Praise",
        back_populates="recipient",
        cascade="all, delete-orphan",
        foreign_keys="[Praise.recipient_id]"
    )
