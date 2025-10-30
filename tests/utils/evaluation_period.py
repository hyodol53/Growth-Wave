from sqlalchemy.orm import Session
from app.models.evaluation import EvaluationPeriod
from datetime import date, timedelta
from tests.utils.common import random_lower_string

def create_random_evaluation_period(db: Session) -> EvaluationPeriod:
    start_date = date.today() - timedelta(days=1)
    end_date = date.today() + timedelta(days=1)
    period = EvaluationPeriod(
        name=f"Test Period {random_lower_string()}",
        start_date=start_date,
        end_date=end_date
    )
    db.add(period)
    db.commit()
    db.refresh(period)
    return period
