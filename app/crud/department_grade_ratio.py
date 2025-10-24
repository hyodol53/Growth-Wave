from app.crud.base import CRUDBase
from app.models.evaluation import DepartmentGradeRatio
from app.schemas.evaluation import DepartmentGradeRatioCreate, DepartmentGradeRatioUpdate
from sqlalchemy.orm import Session

class CRUDDepartmentGradeRatio(CRUDBase[DepartmentGradeRatio, DepartmentGradeRatioCreate, DepartmentGradeRatioUpdate]):
    def get_by_grade(self, db: Session, *, department_grade: str) -> DepartmentGradeRatio | None:
        return db.query(DepartmentGradeRatio).filter(DepartmentGradeRatio.department_grade == department_grade).first()


department_grade_ratio = CRUDDepartmentGradeRatio(DepartmentGradeRatio)
