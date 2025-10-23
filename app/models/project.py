from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    # A project is owned/managed by an organization (e.g., a '실')
    owner_org_id = Column(Integer, ForeignKey("organizations.id"))
    owner_org = relationship("Organization", back_populates="projects")

    # Members associated with this project
    project_members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
