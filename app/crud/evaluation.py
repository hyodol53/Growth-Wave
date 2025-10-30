from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.evaluation import EvaluationWeight, DepartmentEvaluation
from app.schemas.evaluation import EvaluationWeightCreate, EvaluationWeightUpdate, DepartmentEvaluationCreate, DepartmentEvaluationUpdate
from app.models.user import UserRole

class CRUDEvaluationWeight(CRUDBase[EvaluationWeight, EvaluationWeightCreate, EvaluationWeightUpdate]):

    def get_multi_by_role(self, db: Session, *, role: UserRole) -> List[EvaluationWeight]:

        return db.query(EvaluationWeight).filter(EvaluationWeight.role == role).all()

evaluation_weight = CRUDEvaluationWeight(EvaluationWeight)

class CRUDDepartmentEvaluation(CRUDBase[DepartmentEvaluation, DepartmentEvaluationCreate, DepartmentEvaluationUpdate]):
    def upsert_department_evaluation(self, db: Session, *, eval_in: DepartmentEvaluationCreate):
        db_obj = db.query(DepartmentEvaluation).filter(
            DepartmentEvaluation.department_id == eval_in.department_id,
            DepartmentEvaluation.evaluation_period_id == eval_in.evaluation_period_id
        ).first()

        if db_obj:
            db_obj.grade = eval_in.grade
        else:
            db_obj = DepartmentEvaluation(**eval_in.dict())
            db.add(db_obj)

        db.commit()
        db.refresh(db_obj)
        return db_obj

department_evaluation = CRUDDepartmentEvaluation(DepartmentEvaluation)
