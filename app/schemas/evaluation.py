from pydantic import BaseModel, ConfigDict
from datetime import date
from app.models.user import UserRole
from app.models.evaluation import EvaluationItem
from typing import List, Optional

# EvaluationWeight Schemas
class EvaluationWeightBase(BaseModel):
    role: UserRole
    item: EvaluationItem
    weight: float

class EvaluationWeightCreate(EvaluationWeightBase):
    pass

class EvaluationWeightUpdate(EvaluationWeightBase):
    pass

class EvaluationWeightInDB(EvaluationWeightBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class EvaluationWeight(EvaluationWeightInDB):
    pass

# PeerEvaluation Schemas
class PeerEvaluationBase(BaseModel):
    project_id: int
    evaluatee_id: int
    score: int
    comment: Optional[str] = None

class PeerEvaluationCreate(BaseModel):
    evaluations: List[PeerEvaluationBase]

class PeerEvaluationInDBBase(PeerEvaluationBase):
    id: int
    evaluator_id: int
    evaluation_period: str

    model_config = ConfigDict(from_attributes=True)

class PeerEvaluation(PeerEvaluationInDBBase):
    pass

# PmEvaluation Schemas
class PmEvaluationBase(BaseModel):
    project_id: int
    evaluatee_id: int
    score: int
    comment: Optional[str] = None

class PmEvaluationCreate(BaseModel):
    evaluations: List[PmEvaluationBase]

class PmEvaluationInDBBase(PmEvaluationBase):
    id: int
    evaluator_id: int
    evaluation_period: str

    model_config = ConfigDict(from_attributes=True)

class PmEvaluation(PmEvaluationInDBBase):
    pass


# Schema for Admin to create a single PM evaluation for a PM
class PmSelfEvaluationCreate(PmEvaluationBase):
    pass


# QualitativeEvaluation Schemas
class QualitativeEvaluationBase(BaseModel):
    evaluatee_id: int
    score: int
    feedback: Optional[str] = None


class QualitativeEvaluationCreate(BaseModel):
    evaluations: List[QualitativeEvaluationBase]


class QualitativeEvaluationInDBBase(QualitativeEvaluationBase):
    id: int
    evaluator_id: int
    evaluation_period: str

    model_config = ConfigDict(from_attributes=True)


class QualitativeEvaluation(QualitativeEvaluationInDBBase):
    pass


# FinalEvaluation Schemas
class FinalEvaluationBase(BaseModel):
    evaluatee_id: int
    evaluation_period: str
    peer_score: float | None = None
    pm_score: float | None = None
    qualitative_score: float | None = None
    final_score: float
    grade: Optional[str] = None


class FinalEvaluationCreate(FinalEvaluationBase):
    pass


class FinalEvaluationUpdate(FinalEvaluationBase):
    pass


class FinalEvaluationInDB(FinalEvaluationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FinalEvaluation(FinalEvaluationInDB):
    pass

# Request body for calculate_final_evaluations endpoint
class FinalEvaluationCalculateRequest(BaseModel):
    user_ids: Optional[List[int]] = None

# EvaluationPeriod Schemas
class EvaluationPeriodBase(BaseModel):
    name: str
    start_date: date
    end_date: date

class EvaluationPeriodCreate(EvaluationPeriodBase):
    pass

class EvaluationPeriodUpdate(EvaluationPeriodBase):
    pass

class EvaluationPeriodInDB(EvaluationPeriodBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class EvaluationPeriod(EvaluationPeriodInDB):
    is_active: Optional[bool] = None


# DepartmentGradeRatio Schemas
class DepartmentGradeRatioBase(BaseModel):
    department_grade: str
    s_ratio: float
    a_ratio: float

class GradeAdjustment(BaseModel):
    user_id: int
    grade: str

class GradeAdjustmentRequest(BaseModel):
    evaluation_period: str
    adjustments: List[GradeAdjustment]

class DepartmentGradeRatioCreate(DepartmentGradeRatioBase):
    pass

class DepartmentGradeRatioUpdate(DepartmentGradeRatioBase):
    pass

class DepartmentGradeRatioInDB(DepartmentGradeRatioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class DepartmentGradeRatio(DepartmentGradeRatioInDB):
    pass


# Schemas for viewing evaluation results
class PmScoreResult(BaseModel):
    project_name: str
    pm_name: str
    score: int


class MyEvaluationResult(BaseModel):
    evaluation_period: str
    grade: Optional[str] = None
    pm_scores: List[PmScoreResult]


class ManagerEvaluationView(BaseModel):
    final_evaluation: FinalEvaluation
    peer_feedback: List[str]

    model_config = ConfigDict(from_attributes=True)


# Schemas for Evaluation UX Improvement
class MyEvaluationTask(BaseModel):
    project_id: int
    project_name: str
    user_role_in_project: str # "PM" or "MEMBER"


class PeerEvaluationTarget(BaseModel):
    evaluatee_id: int
    evaluatee_name: str
    score: Optional[int] = None
    comment: Optional[str] = None


class PeerEvaluationDetail(BaseModel):
    project_id: int
    project_name: str
    status: str # "NOT_STARTED", "IN_PROGRESS", "COMPLETED"
    peers_to_evaluate: List[PeerEvaluationTarget]


class PmEvaluationTarget(BaseModel):
    evaluatee_id: int
    evaluatee_name: str
    score: Optional[int] = None
    comment: Optional[str] = None


class PmEvaluationDetail(BaseModel):
    project_id: int
    project_name: str
    status: str # "NOT_STARTED", "IN_PROGRESS", "COMPLETED"
    members_to_evaluate: List[PmEvaluationTarget]
