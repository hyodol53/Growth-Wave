from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.evaluation import QualitativeEvaluation
from app.schemas.evaluation import QualitativeEvaluationCreate, QualitativeEvaluationBase

class CRUDQualitativeEvaluation(CRUDBase[QualitativeEvaluation, QualitativeEvaluationCreate, QualitativeEvaluationBase]):
    def get_by_evaluatee(
        self, db: Session, *, evaluatee_id: int, evaluation_period: str
    ) -> QualitativeEvaluation | None:
        return (
            db.query(QualitativeEvaluation)
            .filter(
                QualitativeEvaluation.evaluatee_id == evaluatee_id,
                QualitativeEvaluation.evaluation_period == evaluation_period,
            )
            .first()
        )

    def create_multi(
        self, db: Session, *, evaluations: List[QualitativeEvaluationBase], evaluator_id: int, evaluation_period: str
    ) -> List[QualitativeEvaluation]:
        db_objs = [
            QualitativeEvaluation(
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

qualitative_evaluation = CRUDQualitativeEvaluation(QualitativeEvaluation)
