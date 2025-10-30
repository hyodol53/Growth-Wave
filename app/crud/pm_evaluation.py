from typing import List, Any, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.evaluation import PmEvaluation, EvaluationPeriod
from app.models.project import Project
from app.models.user import User
from app.schemas.evaluation import PmEvaluationCreate, PmEvaluationBase

class CRUDPmEvaluation(CRUDBase[PmEvaluation, PmEvaluationCreate, PmEvaluationBase]):
    def get_for_evaluatee_by_period(
        self, db: Session, *, evaluatee_id: int, evaluation_period: str
    ) -> List[Any]:
        """
        Gets all PM evaluations for an evaluatee for a specific period,
        joining with project and user tables to get project name and PM name.
        """
        return (
            db.query(
                PmEvaluation.score,
                Project.name.label("project_name"),
                User.full_name.label("pm_name"),
            )
            .join(Project, PmEvaluation.project_id == Project.id)
            .join(User, PmEvaluation.evaluator_id == User.id)
            .filter(
                PmEvaluation.evaluatee_id == evaluatee_id,
                PmEvaluation.evaluation_period == evaluation_period,
            )
            .all()
        )

    def get_for_evaluatee_by_project_and_period(
        self, db: Session, *, evaluatee_id: int, project_id: int, period_id: int
    ) -> Optional[PmEvaluation]:
        period = db.query(EvaluationPeriod).filter(EvaluationPeriod.id == period_id).first()
        if not period:
            return None
        return (
            db.query(PmEvaluation)
            .filter(
                PmEvaluation.evaluatee_id == evaluatee_id,
                PmEvaluation.project_id == project_id,
                PmEvaluation.evaluation_period == period.name,
            )
            .first()
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
            comment=obj_in.comment,
            evaluator_id=evaluator_id,
            evaluation_period=evaluation_period,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_evaluator_and_evaluatee(
        self, db: Session, *, project_id: int, evaluator_id: int, evaluatee_id: int, evaluation_period: str
    ) -> PmEvaluation | None:
        return (
            db.query(PmEvaluation)
            .filter(
                PmEvaluation.project_id == project_id,
                PmEvaluation.evaluator_id == evaluator_id,
                PmEvaluation.evaluatee_id == evaluatee_id,
                PmEvaluation.evaluation_period == evaluation_period,
            )
            .first()
        )

    def upsert_multi(
        self, db: Session, *, evaluations: List[PmEvaluationBase], evaluator_id: int, evaluation_period: str
    ) -> List[PmEvaluation]:
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
                new_eval = PmEvaluation(
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
        self, db: Session, *, evaluations: List[PmEvaluationBase], evaluator_id: int, evaluation_period: str
    ) -> List[PmEvaluation]:
        db_objs = [
            PmEvaluation(
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

pm_evaluation = CRUDPmEvaluation(PmEvaluation)