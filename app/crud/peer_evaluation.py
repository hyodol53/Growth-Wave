from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.evaluation import PeerEvaluation
from app.schemas.evaluation import PeerEvaluationCreate, PeerEvaluationBase

class CRUDPeerEvaluation(CRUDBase[PeerEvaluation, PeerEvaluationCreate, PeerEvaluationBase]):
    def get_feedback_for_evaluatee_by_period(
        self, db: Session, *, evaluatee_id: int, evaluation_period: str
    ) -> List[str]:
        """
        Gets all non-empty feedback strings for an evaluatee for a specific period.
        """
        return (
            db.query(PeerEvaluation.comment)
            .filter(
                PeerEvaluation.evaluatee_id == evaluatee_id,
                PeerEvaluation.evaluation_period == evaluation_period,
                PeerEvaluation.comment.isnot(None),
                PeerEvaluation.comment != "",
            )
            .all()
        )

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

    def get_by_evaluator_and_evaluatee(
        self, db: Session, *, project_id: int, evaluator_id: int, evaluatee_id: int, evaluation_period: str
    ) -> PeerEvaluation | None:
        return (
            db.query(PeerEvaluation)
            .filter(
                PeerEvaluation.project_id == project_id,
                PeerEvaluation.evaluator_id == evaluator_id,
                PeerEvaluation.evaluatee_id == evaluatee_id,
                PeerEvaluation.evaluation_period == evaluation_period,
            )
            .first()
        )

    def upsert_multi(
        self, db: Session, *, evaluations: List[PeerEvaluationBase], evaluator_id: int, evaluation_period: str
    ) -> List[PeerEvaluation]:
        upserted_objs = []
        for evaluation in evaluations:
            existing_eval = self.get_by_evaluator_and_evaluatee(
                db,
                project_id=evaluation.project_id,
                evaluator_id=evaluator_id,
                evaluatee_id=evaluation.evaluatee_id,
                evaluation_period=evaluation_period,
            )
            if existing_eval:
                # Update existing evaluation
                existing_eval.score = evaluation.score
                existing_eval.comment = evaluation.comment
                db.add(existing_eval)
                upserted_objs.append(existing_eval)
            else:
                # Create new evaluation
                new_eval = PeerEvaluation(
                    project_id=evaluation.project_id,
                    evaluatee_id=evaluation.evaluatee_id,
                    score=evaluation.score,
                    comment=evaluation.comment,
                    evaluator_id=evaluator_id,
                    evaluation_period=evaluation_period,
                )
                db.add(new_eval)
                upserted_objs.append(new_eval)
        
        db.commit()
        for obj in upserted_objs:
            db.refresh(obj)
        return upserted_objs

    def create_multi(
        self, db: Session, *, evaluations: List[PeerEvaluationBase], evaluator_id: int, evaluation_period: str
    ) -> List[PeerEvaluation]:
        db_objs = [
            PeerEvaluation(
                project_id=evaluation.project_id,
                evaluatee_id=evaluation.evaluatee_id,
                score=evaluation.score,
                comment=evaluation.comment,
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
