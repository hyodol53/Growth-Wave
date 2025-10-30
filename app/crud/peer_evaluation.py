from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.crud.base import CRUDBase
from app.models.evaluation import PeerEvaluation, EvaluationPeriod
from app.schemas.evaluation import PeerEvaluationCreate, PeerEvaluationBase

class CRUDPeerEvaluation(CRUDBase[PeerEvaluation, PeerEvaluationCreate, PeerEvaluationBase]):
    def get_feedback_for_evaluatee_by_period(
        self, db: Session, *, evaluatee_id: int, evaluation_period: str
    ) -> List[str]:
        """
        Gets all non-empty feedback comments for an evaluatee for a specific period across all projects.
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

    def get_feedback_for_evaluatee(
        self, db: Session, *, evaluatee_id: int, project_id: int, period_id: int
    ) -> List[PeerEvaluation]:
        """
        Gets all non-empty feedback for an evaluatee for a specific project and period.
        """
        period = db.query(EvaluationPeriod).filter(EvaluationPeriod.id == period_id).first()
        if not period:
            return []
        return (
            db.query(PeerEvaluation)
            .filter(
                PeerEvaluation.evaluatee_id == evaluatee_id,
                PeerEvaluation.project_id == project_id,
                PeerEvaluation.evaluation_period == period.name,
                PeerEvaluation.comment.isnot(None),
                PeerEvaluation.comment != "",
            )
            .all()
        )

    def get_average_score_for_evaluatee(
        self, db: Session, *, evaluatee_id: int, project_id: int, period_id: int
    ) -> float | None:
        """Calculates the average total score for an evaluatee in a specific project and period."""
        period = db.query(EvaluationPeriod).filter(EvaluationPeriod.id == period_id).first()
        if not period:
            return None
            
        scores_sum = db.query(
            func.sum(
                PeerEvaluation.score_1
                + PeerEvaluation.score_2
                + PeerEvaluation.score_3
                + PeerEvaluation.score_4
                + PeerEvaluation.score_5
                + PeerEvaluation.score_6
                + PeerEvaluation.score_7
            )
        ).filter(
            PeerEvaluation.evaluatee_id == evaluatee_id,
            PeerEvaluation.project_id == project_id,
            PeerEvaluation.evaluation_period == period.name,
        ).scalar()

        count = self.get_count_for_evaluatee(db, evaluatee_id=evaluatee_id, project_id=project_id, period_id=period_id)

        return scores_sum / count if scores_sum is not None and count > 0 else None

    def get_count_for_evaluatee(
        self, db: Session, *, evaluatee_id: int, project_id: int, period_id: int
    ) -> int:
        """Counts the number of evaluations for an evaluatee in a specific project and period."""
        period = db.query(EvaluationPeriod).filter(EvaluationPeriod.id == period_id).first()
        if not period:
            return 0
        return db.query(PeerEvaluation).filter(
            PeerEvaluation.evaluatee_id == evaluatee_id,
            PeerEvaluation.project_id == project_id,
            PeerEvaluation.evaluation_period == period.name,
        ).count()

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

            update_data = {
                "score_1": evaluation.scores[0],
                "score_2": evaluation.scores[1],
                "score_3": evaluation.scores[2],
                "score_4": evaluation.scores[3],
                "score_5": evaluation.scores[4],
                "score_6": evaluation.scores[5],
                "score_7": evaluation.scores[6],
                "comment": evaluation.comment,
            }

            if existing_eval:
                # Update existing evaluation
                for key, value in update_data.items():
                    setattr(existing_eval, key, value)
                db.add(existing_eval)
                upserted_objs.append(existing_eval)
            else:
                # Create new evaluation
                new_eval = PeerEvaluation(
                    project_id=evaluation.project_id,
                    evaluatee_id=evaluation.evaluatee_id,
                    evaluator_id=evaluator_id,
                    evaluation_period=evaluation_period,
                    **update_data
                )
                db.add(new_eval)
                upserted_objs.append(new_eval)
        
        db.commit()
        for obj in upserted_objs:
            db.refresh(obj)
        return upserted_objs

peer_evaluation = CRUDPeerEvaluation(PeerEvaluation)
