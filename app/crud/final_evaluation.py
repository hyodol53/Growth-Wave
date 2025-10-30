from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.evaluation import FinalEvaluation, EvaluationPeriod
from app.schemas.evaluation import FinalEvaluationCreate, FinalEvaluationUpdate

class CRUDFinalEvaluation(CRUDBase[FinalEvaluation, FinalEvaluationCreate, FinalEvaluationUpdate]):
    def get_by_user_and_period(
        self, db: Session, *, evaluatee_id: int, period_id: int
    ) -> FinalEvaluation | None:
        period = db.query(EvaluationPeriod).filter(EvaluationPeriod.id == period_id).first()
        if not period:
            return None
        return (
            db.query(FinalEvaluation)
            .filter(
                FinalEvaluation.evaluatee_id == evaluatee_id,
                FinalEvaluation.evaluation_period == period.name,
            )
            .first()
        )

final_evaluation = CRUDFinalEvaluation(FinalEvaluation)
