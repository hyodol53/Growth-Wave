from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    # The project is managed by a Project Manager (PM)
    pm_id = Column(Integer, ForeignKey("users.id"))
    pm = relationship("User", back_populates="projects_managed")

    # Members associated with this project
    project_members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
