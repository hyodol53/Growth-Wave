from app.crud.base import CRUDBase
from app.models.evaluation import EvaluationPeriod
from app.schemas.evaluation import EvaluationPeriodCreate, EvaluationPeriodUpdate
from sqlalchemy.orm import Session
from datetime import date


class CRUDEvaluationPeriod(CRUDBase[EvaluationPeriod, EvaluationPeriodCreate, EvaluationPeriodUpdate]):
    def get_active_period(self, db: Session) -> EvaluationPeriod | None:
        """
        Find the currently active evaluation period.
        """
        today = date.today()
        return db.query(EvaluationPeriod).filter(
            EvaluationPeriod.start_date <= today,
            EvaluationPeriod.end_date >= today
        ).first()


evaluation_period = CRUDEvaluationPeriod(EvaluationPeriod)
