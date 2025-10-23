from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.evaluation import FinalEvaluation
from app.schemas.evaluation import FinalEvaluationCreate, FinalEvaluationUpdate

class CRUDFinalEvaluation(CRUDBase[FinalEvaluation, FinalEvaluationCreate, FinalEvaluationUpdate]):
    def get_by_evaluatee_and_period(
        self, db: Session, *, evaluatee_id: int, evaluation_period: str
    ) -> FinalEvaluation | None:
        return (
            db.query(FinalEvaluation)
            .filter(
                FinalEvaluation.evaluatee_id == evaluatee_id,
                FinalEvaluation.evaluation_period == evaluation_period,
            )
            .first()
        )

final_evaluation = CRUDFinalEvaluation(FinalEvaluation)
