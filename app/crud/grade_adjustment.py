from app import crud, models
from typing import List, Dict
from app.schemas.evaluation import GradeAdjustment
from sqlalchemy.orm import Session
from app.exceptions import GradeAdjustmentError, GradeTOExceededError
import math

def adjust_grades_for_department(
    db: Session,
    *,
    department_id: int,
    evaluation_period: str,
    adjustments: List[GradeAdjustment],
    current_user_role: models.UserRole,
) -> List[models.FinalEvaluation]:
    """
    Adjusts grades for all users in a department, ensuring B+/B- balance and TO limits.
    """
    # 1. Get the department and its users
    parent_org = crud.organization.organization.get(db, id=department_id)
    if not parent_org:
        raise GradeAdjustmentError(f"Department with id {department_id} not found.")
    org_and_descendants = [parent_org] + crud.organization.get_all_descendant_orgs(db, department_id)
    dept_user_ids = [user.id for org in org_and_descendants for user in org.members]
    
    # 2. Get all final evaluations for these users in the period
    all_evals = (
        db.query(models.FinalEvaluation)
        .filter(
            models.FinalEvaluation.evaluatee_id.in_(dept_user_ids),
            models.FinalEvaluation.evaluation_period == evaluation_period,
        )
        .all()
    )

    # 3. Create a map of proposed changes
    adjustment_map: Dict[int, str] = {adj.user_id: adj.grade for adj in adjustments}

    # 4. Apply proposed changes to a temporary copy of the evaluations
    temp_grades: Dict[int, str | None] = {ev.evaluatee_id: ev.grade for ev in all_evals}
    for user_id, new_grade in adjustment_map.items():
        if user_id in temp_grades:
            temp_grades[user_id] = new_grade

    # 5. TO Validation for DEPT_HEAD
    if current_user_role == models.UserRole.DEPT_HEAD:
        # Get the evaluation period object to find the period_id
        period = crud.evaluation_period.get_by_name(db, name=evaluation_period)
        if not period:
            raise GradeAdjustmentError(f"Evaluation period '{evaluation_period}' not found.")

        # Get the department's grade for the specific period from the DepartmentEvaluation table
        dept_eval = db.query(models.DepartmentEvaluation).filter(
            models.DepartmentEvaluation.department_id == department_id,
            models.DepartmentEvaluation.evaluation_period_id == period.id
        ).first()

        if not dept_eval or not dept_eval.grade:
            raise GradeTOExceededError("Department grade is not set for the selected period.")
        
        department_grade = dept_eval.grade
        
        ratio = crud.department_grade_ratio.get_by_grade(db, department_grade=department_grade)
        if not ratio:
            raise GradeTOExceededError(f"Grade ratio for department grade '{department_grade}' not found.")

        num_employees = len(dept_user_ids)
        s_to = math.floor(num_employees * (ratio.s_ratio / 100.0))
        a_to = math.floor(num_employees * (ratio.a_ratio / 100.0))

        s_count = sum(1 for grade in temp_grades.values() if grade == "S")
        a_count = sum(1 for grade in temp_grades.values() if grade == "A")

        if s_count > s_to:
            raise GradeTOExceededError(f"Number of S grades ({s_count}) exceeds the limit ({s_to}).")
        if a_count > a_to:
            raise GradeTOExceededError(f"Number of A grades ({a_count}) exceeds the limit ({a_to}).")

    # 6. B+/B- Validation for DEPT_HEAD
    if current_user_role == models.UserRole.DEPT_HEAD:
        b_plus_count = sum(1 for grade in temp_grades.values() if grade == "B+")
        b_minus_count = sum(1 for grade in temp_grades.values() if grade == "B-")
        if b_plus_count != b_minus_count:
            raise GradeAdjustmentError("The number of B+ and B- grades must be equal.")

    # 7. If validation passes, update the database
    updated_evaluations = []
    for user_id, new_grade in adjustment_map.items():
        evaluation_to_update = next((ev for ev in all_evals if ev.evaluatee_id == user_id), None)
        if evaluation_to_update:
            updated_eval = crud.final_evaluation.update(
                db, db_obj=evaluation_to_update, obj_in={"grade": new_grade}
            )
            updated_evaluations.append(updated_eval)

    # Return the evaluations that were actually updated
    return updated_evaluations
