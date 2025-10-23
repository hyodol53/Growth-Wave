from sqlalchemy.orm import Session
from app import crud
from app.models.evaluation import EvaluationWeight, PeerEvaluation, PmEvaluation, QualitativeEvaluation, EvaluationItem
from app.schemas.evaluation import EvaluationWeightCreate, PeerEvaluationCreate, PmEvaluationCreate, QualitativeEvaluationCreate, PeerEvaluationBase, PmEvaluationBase, QualitativeEvaluationBase
from app.schemas.user import UserRole

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
    feedback: str = "Good job!",
    evaluation_period: str = "2025-H1"
) -> PeerEvaluation:
    peer_eval_base = PeerEvaluationBase(
        project_id=project_id,
        evaluatee_id=evaluatee_id,
        score=score
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
