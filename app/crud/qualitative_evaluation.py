from typing import List
from sqlalchemy.orm import Session, aliased, joinedload
from app.crud.base import CRUDBase
from app.models.evaluation import QualitativeEvaluation, EvaluationPeriod
from app.schemas.evaluation import QualitativeEvaluationCreate, QualitativeEvaluationBase
from app import crud
from app.models.user import User, UserRole
from app.models.organization import Organization

class CRUDQualitativeEvaluation(CRUDBase[QualitativeEvaluation, QualitativeEvaluationCreate, QualitativeEvaluationBase]):
    def get_by_evaluatee_and_period(
        self, db: Session, *, evaluatee_id: int, period_id: int
    ) -> QualitativeEvaluation | None:
        period = db.query(EvaluationPeriod).filter(EvaluationPeriod.id == period_id).first()
        if not period:
            return None
        return (
            db.query(QualitativeEvaluation)
            .filter(
                QualitativeEvaluation.evaluatee_id == evaluatee_id,
                QualitativeEvaluation.evaluation_period == period.name,
            )
            .first()
        )

    def upsert_multi(
        self, db: Session, *, evaluations: List[QualitativeEvaluationBase], evaluator_id: int, evaluation_period: str
    ) -> List[QualitativeEvaluation]:
        
        updated_and_created_evaluations = []

        for evaluation in evaluations:
            # Check if an evaluation already exists
            existing_eval = db.query(QualitativeEvaluation).filter(
                QualitativeEvaluation.evaluator_id == evaluator_id,
                QualitativeEvaluation.evaluatee_id == evaluation.evaluatee_id,
                QualitativeEvaluation.evaluation_period == evaluation_period
            ).first()

            if existing_eval:
                # Update existing evaluation
                existing_eval.qualitative_score = evaluation.qualitative_score
                existing_eval.department_contribution_score = evaluation.department_contribution_score
                existing_eval.feedback = evaluation.feedback
                db.add(existing_eval)
                updated_and_created_evaluations.append(existing_eval)
            else:
                # Create new evaluation
                new_eval = QualitativeEvaluation(
                    evaluator_id=evaluator_id,
                    evaluatee_id=evaluation.evaluatee_id,
                    evaluation_period=evaluation_period,
                    qualitative_score=evaluation.qualitative_score,
                    department_contribution_score=evaluation.department_contribution_score,
                    feedback=evaluation.feedback,
                )
                db.add(new_eval)
                updated_and_created_evaluations.append(new_eval)

        db.commit()
        for eval_obj in updated_and_created_evaluations:
            db.refresh(eval_obj)
            
        return updated_and_created_evaluations

    def get_members_to_evaluate(self, db: Session, *, evaluator: User) -> List[User]:
        active_period = crud.evaluation_period.get_active_period(db)
        if not active_period:
            return []

        subordinates = crud.user.user.get_subordinates(db, user_id=evaluator.id)
        
        target_evaluatees = []
        if evaluator.role == UserRole.TEAM_LEAD:
            target_evaluatees = subordinates
        elif evaluator.role == UserRole.DEPT_HEAD:
            target_evaluatees = [
                sub for sub in subordinates if sub.role == UserRole.TEAM_LEAD
            ]
        else:
            return []

        if not target_evaluatees:
            return []

        target_ids = [user.id for user in target_evaluatees]

        # Alias for the specific evaluation by the current evaluator
        CurrentEvaluation = aliased(QualitativeEvaluation)

        # Query users and left join their evaluations for the current period by the current evaluator
        results = (
            db.query(
                User.id.label("evaluatee_id"),
                User.full_name.label("evaluatee_name"),
                User.title,
                Organization.name.label("organization_name"),
                CurrentEvaluation.qualitative_score,
                CurrentEvaluation.department_contribution_score,
                CurrentEvaluation.feedback,
            )
            .outerjoin(Organization, User.organization_id == Organization.id)
            .outerjoin(
                CurrentEvaluation,
                (User.id == CurrentEvaluation.evaluatee_id)
                & (CurrentEvaluation.evaluator_id == evaluator.id)
                & (CurrentEvaluation.evaluation_period == active_period.name),
            )
            .filter(User.id.in_(target_ids))
            .all()
        )
        return results


qualitative_evaluation = CRUDQualitativeEvaluation(QualitativeEvaluation)
