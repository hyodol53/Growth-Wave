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
from datetime import date, timedelta
from tests.utils.utils import random_lower_string
from typing import Optional

def create_random_evaluation_period(
    db: Session, 
    *, 
    name: Optional[str] = None, 
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None
) -> EvaluationPeriod:
    if name is None:
        name = f"Test Period {random_lower_string()}"
    if start_date is None:
        start_date = date.today() - timedelta(days=1)
    if end_date is None:
        end_date = date.today() + timedelta(days=1)
    period_in = EvaluationPeriodCreate(name=name, start_date=start_date, end_date=end_date)
    return crud.evaluation_period.create(db=db, obj_in=period_in)

def create_random_evaluation_weight(
    db: Session, 
    role: UserRole = UserRole.EMPLOYEE, 
    item: EvaluationItem = EvaluationItem.PEER_REVIEW, 
    weight: float = 50.0
) -> EvaluationWeight:
    weight_in = EvaluationWeightCreate(role=role.value, item=item, weight=weight)
    return crud.evaluation.evaluation_weight.create(db=db, obj_in=weight_in)

def create_random_peer_evaluation(
    db: Session, 
    evaluator_id: int, 
    evaluatee_id: int, 
    project_id: int, 
    score: int = 70,
    comment: str = "Good job!",
    evaluation_period: str = "2025-H1"
) -> PeerEvaluation:
    max_scores = [20, 20, 10, 10, 10, 10, 20]
    scores = [int(s * score / 100) for s in max_scores]
    diff = score - sum(scores)
    scores[0] += diff

    peer_eval_base = PeerEvaluationBase(
        project_id=project_id,
        evaluatee_id=evaluatee_id,
        scores=scores,
        comment=comment
    )
    peer_eval_in = PeerEvaluationCreate(evaluations=[peer_eval_base])
    return crud.peer_evaluation.peer_evaluation.upsert_multi(
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
    qualitative_score: int = 18,
    department_contribution_score: int = 8,
    feedback: str = "Excellent performance",
    evaluation_period: str = "2025-H1"
) -> QualitativeEvaluation:
    qual_eval_base = QualitativeEvaluationBase(
        evaluatee_id=evaluatee_id,
        qualitative_score=qualitative_score,
        department_contribution_score=department_contribution_score,
        feedback=feedback
    )
    qual_eval_in = QualitativeEvaluationCreate(evaluations=[qual_eval_base])
    return crud.qualitative_evaluation.qualitative_evaluation.create_multi(
        db, evaluations=qual_eval_in.evaluations, evaluator_id=evaluator_id, evaluation_period=evaluation_period
    )[0]

def create_random_final_evaluation(
    db: Session,
    *,
    evaluatee_id: int,
    final_score: float,
    evaluation_period: Optional[str] = None,
    period_id: Optional[int] = None,
    grade: str | None = None,
) -> FinalEvaluation:
    if evaluation_period is None:
        if period_id:
            period = crud.evaluation_period.get(db, id=period_id)
            if not period:
                 raise ValueError("period not found")
            evaluation_period = period.name
        else:
            evaluation_period = f"{date.today().year}-H{1 if date.today().month <= 6 else 2}"

    # Ensure the evaluation period exists
    period = crud.evaluation_period.get_by_name(db, name=evaluation_period)
    if not period:
        year_str, half_str = evaluation_period.split("-H")
        year = int(year_str)
        if half_str == "1":
            start_date = date(year, 1, 1)
            end_date = date(year, 6, 30)
        else:
            start_date = date(year, 7, 1)
            end_date = date(year, 12, 31)
        create_random_evaluation_period(db, name=evaluation_period, start_date=start_date, end_date=end_date)
            
    final_eval_in = FinalEvaluationCreate(
        evaluatee_id=evaluatee_id, 
        evaluation_period=evaluation_period, 
        final_score=final_score,
        grade=grade
    )
    return crud.final_evaluation.create(db, obj_in=final_eval_in)
