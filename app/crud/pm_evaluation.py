from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.evaluation import PmEvaluation
from app.schemas.evaluation import PmEvaluationCreate, PmEvaluationBase

class CRUDPmEvaluation(CRUDBase[PmEvaluation, PmEvaluationCreate, PmEvaluationBase]):
    def get_by_project_and_evaluatee(
        self, db: Session, *, project_id: int, evaluatee_id: int, evaluation_period: str
    ) -> List[PmEvaluation]:
        return (
            db.query(PmEvaluation)
            .filter(
                PmEvaluation.project_id == project_id,
                PmEvaluation.evaluatee_id == evaluatee_id,
                PmEvaluation.evaluation_period == evaluation_period,
            )
            .all()
        )

    def get_by_evaluatee(self, db: Session, *, evaluatee_id: int, evaluation_period: str) -> List[PmEvaluation]:
        return (
            db.query(PmEvaluation)
            .filter(
                PmEvaluation.evaluatee_id == evaluatee_id,
                PmEvaluation.evaluation_period == evaluation_period,
            )
            .all()
        )

    def create(self, db: Session, *, obj_in: PmEvaluationBase, evaluator_id: int, evaluation_period: str) -> PmEvaluation:
        db_obj = PmEvaluation(
            project_id=obj_in.project_id,
            evaluatee_id=obj_in.evaluatee_id,
            score=obj_in.score,
            evaluator_id=evaluator_id,
            evaluation_period=evaluation_period,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_multi(
        self, db: Session, *, evaluations: List[PmEvaluationBase], evaluator_id: int, evaluation_period: str
    ) -> List[PmEvaluation]:
        db_objs = [
            PmEvaluation(
                project_id=evaluation.project_id,
                evaluatee_id=evaluation.evaluatee_id,
                score=evaluation.score,
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

pm_evaluation = CRUDPmEvaluation(PmEvaluation)