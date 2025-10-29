from sqlalchemy.orm import Session
from app import crud
from app.models.evaluation import (
    EvaluationWeight, PeerEvaluation, PmEvaluation, QualitativeEvaluation, 
    EvaluationItem, FinalEvaluation, EvaluationPeriod
)
from app.schemas.evaluation import (
    EvaluationWeightCreate, PeerEvaluationCreate, PmEvaluationCreate, 
    QualitativeEvaluationCreate, PeerEvaluationBase, PmEvaluationBase, 
    QualitativeEvaluationBase, FinalEvaluationCreate, EvaluationPeriodCreate
)
from app.schemas.user import UserRole
from datetime import date

def create_random_evaluation_period(
    db: Session, *, name: str, start_date: date, end_date: date
) -> EvaluationPeriod:
    period_in = EvaluationPeriodCreate(name=name, start_date=start_date, end_date=end_date)
    return crud.evaluation_period.create(db=db, obj_in=period_in)

def create_random_evaluation_weight(
    db: Session, 
    role: UserRole = UserRole.EMPLOYEE, 
    item: EvaluationItem = EvaluationItem.PEER_REVIEW, 
    weight: float = 50.0
) -> EvaluationWeight:
    weight_in = EvaluationWeightCreate(role=role, item=item, weight=weight)
    return crud.evaluation.evaluation_weight.create(db=db, obj_in=weight_in)

def create_random_peer_evaluation(
    db: Session, 
    evaluator_id: int, 
    evaluatee_id: int, 
    project_id: int, 
    score: float = 70.0,
    comment: str = "Good job!",
    evaluation_period: str = "2025-H1"
) -> PeerEvaluation:
    peer_eval_base = PeerEvaluationBase(
        project_id=project_id,
        evaluatee_id=evaluatee_id,
        score=score,
        comment=comment
    )
    peer_eval_in = PeerEvaluationCreate(evaluations=[peer_eval_base])
    return crud.peer_evaluation.peer_evaluation.create_multi(
        db, evaluations=peer_eval_in.evaluations, evaluator_id=evaluator_id, evaluation_period=evaluation_period
    )[0]

def create_random_pm_evaluation(
    db: Session, 
    evaluator_id: int, 
    evaluatee_id: int, 
    project_id: int, 
    score: float = 80.0,
    evaluation_period: str = "2025-H1"
) -> PmEvaluation:
    pm_eval_base = PmEvaluationBase(
        project_id=project_id,
        evaluatee_id=evaluatee_id,
        score=score
    )
    pm_eval_in = PmEvaluationCreate(evaluations=[pm_eval_base])
    return crud.pm_evaluation.pm_evaluation.create_multi(
        db, evaluations=pm_eval_in.evaluations, evaluator_id=evaluator_id, evaluation_period=evaluation_period
    )[0]

def create_random_qualitative_evaluation(
    db: Session, 
    evaluator_id: int, 
    evaluatee_id: int, 
    score: float = 90.0,
    feedback: str = "Excellent performance",
    evaluation_period: str = "2025-H1"
) -> QualitativeEvaluation:
    qual_eval_base = QualitativeEvaluationBase(
        evaluatee_id=evaluatee_id,
        score=score
    )
    qual_eval_in = QualitativeEvaluationCreate(evaluations=[qual_eval_base])
    return crud.qualitative_evaluation.qualitative_evaluation.create_multi(
        db, evaluations=qual_eval_in.evaluations, evaluator_id=evaluator_id, evaluation_period=evaluation_period
    )[0]

def create_random_final_evaluation(
    db: Session,
    *,
    evaluatee_id: int,
    evaluation_period: str,
    final_score: float,
    grade: str | None = None,
) -> FinalEvaluation:
    final_eval_in = FinalEvaluationCreate(
        evaluatee_id=evaluatee_id, 
        evaluation_period=evaluation_period, 
        final_score=final_score,
        grade=grade
    )
    return crud.final_evaluation.create(db, obj_in=final_eval_in)
