from sqlalchemy import Column, Integer, String, Float, Enum as SQLAlchemyEnum, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from app.core.database import Base
from app.models.user import UserRole
import enum

class EvaluationItem(str, enum.Enum):
    PEER_REVIEW = "peer_review"
    PM_REVIEW = "pm_review"
    QUALITATIVE_REVIEW = "qualitative_review"

class EvaluationWeight(Base):
    __tablename__ = "evaluation_weights"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
    item = Column(SQLAlchemyEnum(EvaluationItem), nullable=False)
    weight = Column(Float, nullable=False)

    __table_args__ = {'extend_existing': True}

class PeerEvaluation(Base):
    __tablename__ = "peer_evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    evaluator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    evaluatee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    score_1: Mapped[int] = mapped_column(Integer, nullable=False)
    score_2: Mapped[int] = mapped_column(Integer, nullable=False)
    score_3: Mapped[int] = mapped_column(Integer, nullable=False)
    score_4: Mapped[int] = mapped_column(Integer, nullable=False)
    score_5: Mapped[int] = mapped_column(Integer, nullable=False)
    score_6: Mapped[int] = mapped_column(Integer, nullable=False)
    score_7: Mapped[int] = mapped_column(Integer, nullable=False)
    evaluation_period: Mapped[str] = mapped_column(String, nullable=False)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)

    project = relationship("Project", back_populates="peer_evaluations")
    evaluator = relationship("User", foreign_keys=lambda: PeerEvaluation.evaluator_id)
    evaluatee = relationship("User", foreign_keys=lambda: PeerEvaluation.evaluatee_id)

    @property
    def scores(self) -> List[int]:
        return [
            self.score_1,
            self.score_2,
            self.score_3,
            self.score_4,
            self.score_5,
            self.score_6,
            self.score_7,
        ]

    __table_args__ = {'extend_existing': True}

class PmEvaluation(Base):
    __tablename__ = "pm_evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    evaluator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)  # PM
    evaluatee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    evaluation_period: Mapped[str] = mapped_column(String, nullable=False)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)

    project = relationship("Project", back_populates="pm_evaluations")
    evaluator = relationship("User", foreign_keys=lambda: PmEvaluation.evaluator_id)
    evaluatee = relationship("User", foreign_keys=lambda: PmEvaluation.evaluatee_id)

    __table_args__ = {'extend_existing': True}

class QualitativeEvaluation(Base):
    __tablename__ = "qualitative_evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    evaluator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)  # Team Lead or Dept Head
    evaluatee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    qualitative_score: Mapped[int] = mapped_column(Integer, nullable=False)
    department_contribution_score: Mapped[int] = mapped_column(Integer, nullable=False)
    feedback: Mapped[str | None] = mapped_column(String, nullable=True)
    evaluation_period: Mapped[str] = mapped_column(String, nullable=False)

    evaluator: Mapped["User"] = relationship("User", foreign_keys=lambda: QualitativeEvaluation.evaluator_id)
    evaluatee: Mapped["User"] = relationship("User", foreign_keys=lambda: QualitativeEvaluation.evaluatee_id)

    __table_args__ = {'extend_existing': True}

class FinalEvaluation(Base):
    __tablename__ = "final_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    evaluatee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    evaluation_period = Column(String, nullable=False)

    peer_score = Column(Float)
    pm_score = Column(Float)
    qualitative_score = Column(Float)
    final_score = Column(Float, nullable=False)
    grade = Column(String, nullable=True)

    evaluatee = relationship("User")

    __table_args__ = {'extend_existing': True}

class EvaluationPeriod(Base):
    __tablename__ = "evaluation_periods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    projects = relationship("Project", back_populates="evaluation_period")
    department_evaluations = relationship("DepartmentEvaluation", back_populates="evaluation_period")


    __table_args__ = {'extend_existing': True}


class DepartmentGradeRatio(Base):
    __tablename__ = "department_grade_ratios"

    id = Column(Integer, primary_key=True, index=True)
    department_grade = Column(String, unique=True, index=True, nullable=False)
    s_ratio = Column(Float, nullable=False)
    a_ratio = Column(Float, nullable=False)

    __table_args__ = {'extend_existing': True}


class DepartmentEvaluation(Base):
    __tablename__ = "department_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    grade = Column(String, nullable=False)
    evaluation_period_id = Column(Integer, ForeignKey("evaluation_periods.id"), nullable=False)

    department = relationship("Organization", back_populates="department_evaluations")
    evaluation_period = relationship("EvaluationPeriod", back_populates="department_evaluations")

    __table_args__ = (
        UniqueConstraint('department_id', 'evaluation_period_id', name='_dept_eval_period_uc'),
        {'extend_existing': True}
    )