from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.evaluation import EvaluationWeight
from app.schemas.evaluation import EvaluationWeightCreate, EvaluationWeightUpdate
from app.models.user import UserRole

class CRUDEvaluationWeight(CRUDBase[EvaluationWeight, EvaluationWeightCreate, EvaluationWeightUpdate]):

    def get_multi_by_role(self, db: Session, *, role: UserRole) -> List[EvaluationWeight]:

        return db.query(EvaluationWeight).filter(EvaluationWeight.role == role).all()



    pass

evaluation_weight = CRUDEvaluationWeight(EvaluationWeight)
