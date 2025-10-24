from app.crud.base import CRUDBase
from app.models.evaluation import EvaluationPeriod
from app.schemas.evaluation import EvaluationPeriodCreate, EvaluationPeriodUpdate


class CRUDEvaluationPeriod(CRUDBase[EvaluationPeriod, EvaluationPeriodCreate, EvaluationPeriodUpdate]):
    pass


evaluation_period = CRUDEvaluationPeriod(EvaluationPeriod)
