from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from app import crud, models, schemas
from app.api import deps
import datetime
from app.schemas.evaluation import FinalEvaluationCalculateRequest

router = APIRouter()

@router.post("/", response_model=schemas.EvaluationWeight)
def create_evaluation_weight(
    *,
    db: Session = Depends(deps.get_db),
    evaluation_weight_in: schemas.EvaluationWeightCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    """
    Create new evaluation weight.
    """
    evaluation_weight = crud.evaluation.evaluation_weight.create(db, obj_in=evaluation_weight_in)
    return evaluation_weight

@router.post("/peer-evaluations/", response_model=List[schemas.PeerEvaluation])
def create_peer_evaluations(
    *,
    db: Session = Depends(deps.get_db),
    evaluations_in: schemas.PeerEvaluationCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new peer evaluations for a user.
    """
    # FR-A-3.1: The average of the scores given cannot exceed 70.
    total_score = sum(e.score for e in evaluations_in.evaluations)
    if total_score / len(evaluations_in.evaluations) > 70:
        raise HTTPException(
            status_code=400,
            detail="Average score cannot exceed 70.",
        )

    # TODO: Add more validation
    # - Check if the evaluator and evaluatee are in the same project.
    # - Check if the evaluation period is active.
    # - Check for duplicate evaluations.

    evaluation_period = f"{datetime.date.today().year}-H{1 if datetime.date.today().month <= 6 else 2}"

    return crud.peer_evaluation.peer_evaluation.create_multi(
        db, evaluations=evaluations_in.evaluations, evaluator_id=current_user.id, evaluation_period=evaluation_period
    )

@router.post("/pm-evaluations/", response_model=List[schemas.PmEvaluation])
def create_pm_evaluations(
    *,
    db: Session = Depends(deps.get_db),
    evaluations_in: schemas.PmEvaluationCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new PM evaluations for project members.
    """
    # TODO: Add more validation
    # - Check if the evaluation period is active.
    # - Check for duplicate evaluations.

    for evaluation in evaluations_in.evaluations:
        # Check if the evaluator is a PM of the project
        project_member = crud.project_member.project_member.get_by_user_and_project(
            db, user_id=current_user.id, project_id=evaluation.project_id
        )
        if not project_member or not project_member.is_pm:
            raise HTTPException(
                status_code=403,
                detail="User is not a Project Manager for this project.",
            )

        # Check if the score is valid
        if not 0 <= evaluation.score <= 100:
            raise HTTPException(
                status_code=400,
                detail="Score must be between 0 and 100.",
            )

    evaluation_period = f"{datetime.date.today().year}-H{1 if datetime.date.today().month <= 6 else 2}"

    return crud.pm_evaluation.pm_evaluation.create_multi(
        db, evaluations=evaluations_in.evaluations, evaluator_id=current_user.id, evaluation_period=evaluation_period
    )


@router.post("/pm-self-evaluation/", response_model=schemas.PmEvaluation)
def create_pm_self_evaluation(
    *,
    db: Session = Depends(deps.get_db),
    evaluation_in: schemas.PmSelfEvaluationCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Create a single PM evaluation, typically for a PM's self-evaluation by a director.
    Accessible only by admin users.
    """
    # Check if the score is valid
    if not 0 <= evaluation_in.score <= 100:
        raise HTTPException(
            status_code=400,
            detail="Score must be between 0 and 100.",
        )

    evaluation_period = f"{datetime.date.today().year}-H{1 if datetime.date.today().month <= 6 else 2}"

    # Use the base CRUD create method for a single object
    db_obj = crud.pm_evaluation.pm_evaluation.create(
        db, obj_in=evaluation_in, evaluator_id=current_user.id, evaluation_period=evaluation_period
    )
    return db_obj


@router.post("/qualitative-evaluations/", response_model=List[schemas.QualitativeEvaluation])
def create_qualitative_evaluations(
    *,
    db: Session = Depends(deps.get_db),
    evaluations_in: schemas.QualitativeEvaluationCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new qualitative evaluations for team/department members.
    """
    # FR-A-3.5: Team lead/Dept head can evaluate their members.
    if current_user.role not in [models.UserRole.TEAM_LEAD, models.UserRole.DEPT_HEAD]:
        raise HTTPException(
            status_code=403,
            detail="User does not have the right to perform qualitative evaluations.",
        )

    # Get all users in the evaluator's organization and sub-organizations
    subordinate_ids = {user.id for user in crud.user.user.get_subordinates(db, user_id=current_user.id)}

    for evaluation in evaluations_in.evaluations:
        # Check if the evaluatee is a subordinate of the evaluator
        if evaluation.evaluatee_id not in subordinate_ids:
            raise HTTPException(
                status_code=403,
                detail=f"User {evaluation.evaluatee_id} is not a subordinate of the evaluator.",
            )

        # Check if the score is valid
        if not 0 <= evaluation.score <= 100:
            raise HTTPException(
                status_code=400,
                detail="Score must be between 0 and 100.",
            )

    evaluation_period = f"{datetime.date.today().year}-H{1 if datetime.date.today().month <= 6 else 2}"

    return crud.qualitative_evaluation.qualitative_evaluation.create_multi(
        db, evaluations=evaluations_in.evaluations, evaluator_id=current_user.id, evaluation_period=evaluation_period
    )


@router.get("/", response_model=List[schemas.EvaluationWeight])
def read_evaluation_weights(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Retrieve evaluation weights.
    """
    evaluation_weights = crud.evaluation.evaluation_weight.get_multi(db, skip=skip, limit=limit)
    return evaluation_weights

@router.put("/{id}", response_model=schemas.EvaluationWeight)
def update_evaluation_weight(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    evaluation_weight_in: schemas.EvaluationWeightUpdate,
    current_user: models.User = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Update an evaluation weight.
    """
    evaluation_weight = crud.evaluation.evaluation_weight.get(db=db, id=id)
    if not evaluation_weight:
        raise HTTPException(status_code=404, detail="Evaluation weight not found")
    evaluation_weight = crud.evaluation.evaluation_weight.update(db=db, db_obj=evaluation_weight, obj_in=evaluation_weight_in)
    return evaluation_weight

@router.delete("/{id}", response_model=schemas.EvaluationWeight)
def delete_evaluation_weight(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Delete an evaluation weight.
    """
    evaluation_weight = crud.evaluation.evaluation_weight.get(db=db, id=id)
    if not evaluation_weight:
        raise HTTPException(status_code=404, detail="Evaluation weight not found")
    evaluation_weight = crud.evaluation.evaluation_weight.remove(db=db, id=id)
    return evaluation_weight


@router.post("/calculate", response_model=List[schemas.FinalEvaluation])
def calculate_final_evaluations(
    *,
    db: Session = Depends(deps.get_db),
    request_body: FinalEvaluationCalculateRequest,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Calculate and store final evaluation scores for specified users or all subordinates.
    Accessible by DEPT_HEAD and ADMIN.
    """
    user_ids = request_body.user_ids

    if current_user.role not in [models.UserRole.DEPT_HEAD, models.UserRole.ADMIN]:
        raise HTTPException(
            status_code=403,
            detail="Not enough privileges to calculate final evaluations.",
        )

    evaluation_period = f"{datetime.date.today().year}-H{1 if datetime.date.today().month <= 6 else 2}"
    calculated_evaluations = []

    target_users: List[models.User] = []
    if user_ids:
        for user_id in user_ids:
            user = crud.user.user.get(db, id=user_id)
            if user:
                target_users.append(user)
    else:
        if current_user.role == models.UserRole.DEPT_HEAD:
            # Calculate for all subordinates of the current DEPT_HEAD
            target_users = crud.user.user.get_subordinates(db, user_id=current_user.id)
        elif current_user.role == models.UserRole.ADMIN:
            # Calculate for all users in the system
            target_users = crud.user.user.get_multi(db)

    for user in target_users:
        final_eval = crud.evaluation_calculator.calculate_and_store_final_scores(
            db, evaluatee=user, evaluation_period=evaluation_period
        )
        if final_eval:
            calculated_evaluations.append(final_eval)

    return calculated_evaluations


@router.post("/evaluation-periods/", response_model=schemas.EvaluationPeriod)
def create_evaluation_period(
    *,
    db: Session = Depends(deps.get_db),
    evaluation_period_in: schemas.EvaluationPeriodCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Create a new evaluation period. (Admin only)
    """
    evaluation_period = crud.evaluation_period.create(db, obj_in=evaluation_period_in)
    return evaluation_period


@router.get("/evaluation-periods/", response_model=List[schemas.EvaluationPeriod])
def read_evaluation_periods(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Retrieve evaluation periods. (Admin only)
    """
    evaluation_periods = crud.evaluation_period.get_multi(db, skip=skip, limit=limit)
    return evaluation_periods


@router.put("/evaluation-periods/{period_id}", response_model=schemas.EvaluationPeriod)
def update_evaluation_period(
    *,
    db: Session = Depends(deps.get_db),
    period_id: int,
    evaluation_period_in: schemas.EvaluationPeriodUpdate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Update an evaluation period. (Admin only)
    """
    evaluation_period = crud.evaluation_period.get(db=db, id=period_id)
    if not evaluation_period:
        raise HTTPException(status_code=404, detail="Evaluation period not found")
    evaluation_period = crud.evaluation_period.update(db=db, db_obj=evaluation_period, obj_in=evaluation_period_in)
    return evaluation_period


@router.delete("/evaluation-periods/{period_id}", response_model=schemas.EvaluationPeriod)
def delete_evaluation_period(
    *,
    db: Session = Depends(deps.get_db),
    period_id: int,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Delete an evaluation period. (Admin only)
    """
    evaluation_period = crud.evaluation_period.get(db=db, id=period_id)
    if not evaluation_period:
        raise HTTPException(status_code=404, detail="Evaluation period not found")
    evaluation_period = crud.evaluation_period.remove(db=db, id=period_id)
    return evaluation_period


@router.post("/department-grade-ratios/", response_model=schemas.DepartmentGradeRatio)
def create_department_grade_ratio(
    *,
    db: Session = Depends(deps.get_db),
    department_grade_ratio_in: schemas.DepartmentGradeRatioCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Create a new department grade ratio. (Admin only)
    """
    department_grade_ratio = crud.department_grade_ratio.create(db, obj_in=department_grade_ratio_in)
    return department_grade_ratio


@router.get("/department-grade-ratios/", response_model=List[schemas.DepartmentGradeRatio])
def read_department_grade_ratios(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Retrieve department grade ratios. (Admin only)
    """
    department_grade_ratios = crud.department_grade_ratio.get_multi(db, skip=skip, limit=limit)
    return department_grade_ratios


@router.put("/department-grade-ratios/{ratio_id}", response_model=schemas.DepartmentGradeRatio)
def update_department_grade_ratio(
    *,
    db: Session = Depends(deps.get_db),
    ratio_id: int,
    department_grade_ratio_in: schemas.DepartmentGradeRatioUpdate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Update a department grade ratio. (Admin only)
    """
    department_grade_ratio = crud.department_grade_ratio.get(db=db, id=ratio_id)
    if not department_grade_ratio:
        raise HTTPException(status_code=404, detail="Department grade ratio not found")
    department_grade_ratio = crud.department_grade_ratio.update(db=db, db_obj=department_grade_ratio, obj_in=department_grade_ratio_in)
    return department_grade_ratio


@router.delete("/department-grade-ratios/{ratio_id}", response_model=schemas.DepartmentGradeRatio)
def delete_department_grade_ratio(
    *,
    db: Session = Depends(deps.get_db),
    ratio_id: int,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Delete a department grade ratio. (Admin only)
    """
    department_grade_ratio = crud.department_grade_ratio.get(db=db, id=ratio_id)
    if not department_grade_ratio:
        raise HTTPException(status_code=404, detail="Department grade ratio not found")
    department_grade_ratio = crud.department_grade_ratio.remove(db=db, id=ratio_id)
    return department_grade_ratio
