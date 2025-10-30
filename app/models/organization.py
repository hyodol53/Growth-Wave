
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Integer, nullable=False)  # 1: 연구소/센터, 2: 실, 3: 팀

    parent_id = Column(Integer, ForeignKey("organizations.id"))
    parent = relationship("Organization", remote_side=[id], back_populates="children")
    children = relationship("Organization", back_populates="parent")

    members = relationship("User", back_populates="organization")

    #department_grade = Column(String, nullable=True)  # S, A, B 등 부서 평가 등급

    department_evaluations = relationship("DepartmentEvaluation", back_populates="department")

