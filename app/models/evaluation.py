from sqlalchemy import Column, Integer, String, Float, Enum as SQLAlchemyEnum, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
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
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    evaluation_period: Mapped[str] = mapped_column(String, nullable=False)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)

    project = relationship("Project")
    evaluator = relationship("User", foreign_keys=lambda: PeerEvaluation.evaluator_id)
    evaluatee = relationship("User", foreign_keys=lambda: PeerEvaluation.evaluatee_id)

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

    project = relationship("Project")
    evaluator = relationship("User", foreign_keys=lambda: PmEvaluation.evaluator_id)
    evaluatee = relationship("User", foreign_keys=lambda: PmEvaluation.evaluatee_id)

    __table_args__ = {'extend_existing': True}

class QualitativeEvaluation(Base):
    __tablename__ = "qualitative_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    evaluator_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Team Lead or Dept Head
    evaluatee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    evaluation_period = Column(String, nullable=False)
    feedback = Column(String, nullable=True)

    evaluator = relationship("User", foreign_keys=lambda: QualitativeEvaluation.evaluator_id)
    evaluatee = relationship("User", foreign_keys=lambda: QualitativeEvaluation.evaluatee_id)

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

    __table_args__ = {'extend_existing': True}


class DepartmentGradeRatio(Base):
    __tablename__ = "department_grade_ratios"

    id = Column(Integer, primary_key=True, index=True)
    department_grade = Column(String, unique=True, index=True, nullable=False)
    s_ratio = Column(Float, nullable=False)
    a_ratio = Column(Float, nullable=False)

    __table_args__ = {'extend_existing': True}