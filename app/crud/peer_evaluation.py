from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.evaluation import PeerEvaluation
from app.schemas.evaluation import PeerEvaluationCreate, PeerEvaluationBase

class CRUDPeerEvaluation(CRUDBase[PeerEvaluation, PeerEvaluationCreate, PeerEvaluationBase]):
    def get_by_project_and_evaluatee(
        self, db: Session, *, project_id: int, evaluatee_id: int, evaluation_period: str
    ) -> List[PeerEvaluation]:
        return (
            db.query(PeerEvaluation)
            .filter(
                PeerEvaluation.project_id == project_id,
                PeerEvaluation.evaluatee_id == evaluatee_id,
                PeerEvaluation.evaluation_period == evaluation_period,
            )
            .all()
        )

    def create_multi(
        self, db: Session, *, evaluations: List[PeerEvaluationBase], evaluator_id: int, evaluation_period: str
    ) -> List[PeerEvaluation]:
        db_objs = [
            PeerEvaluation(
                project_id=evaluation.project_id,
                evaluatee_id=evaluation.evaluatee_id,
                score=evaluation.score,
                feedback=evaluation.feedback,
                evaluator_id=evaluator_id,
                evaluation_period=evaluation_period,
            )
            for evaluation in evaluations
        ]
        db.add_all(db_objs)
        db.commit()
        for db_obj in db_objs:
            db.refresh(db_obj)
        return db_objs

peer_evaluation = CRUDPeerEvaluation(PeerEvaluation)
