from sqlalchemy import Column, Integer, String, Float, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
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

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    evaluator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    evaluatee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    evaluation_period = Column(String, nullable=False)
    feedback = Column(String, nullable=True)

    project = relationship("Project")
    evaluator = relationship("User", foreign_keys=lambda: PeerEvaluation.evaluator_id)
    evaluatee = relationship("User", foreign_keys=lambda: PeerEvaluation.evaluatee_id)

    __table_args__ = {'extend_existing': True}

class PmEvaluation(Base):
    __tablename__ = "pm_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    evaluator_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # PM
    evaluatee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    evaluation_period = Column(String, nullable=False)

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

    evaluatee = relationship("User")

    __table_args__ = {'extend_existing': True}