from app.crud.base import CRUDBase
from app.models.evaluation import DepartmentGradeRatio
from app.schemas.evaluation import DepartmentGradeRatioCreate, DepartmentGradeRatioUpdate


class CRUDDepartmentGradeRatio(CRUDBase[DepartmentGradeRatio, DepartmentGradeRatioCreate, DepartmentGradeRatioUpdate]):
    pass


department_grade_ratio = CRUDDepartmentGradeRatio(DepartmentGradeRatio)
