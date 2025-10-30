from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from app import crud, models, schemas
from app.api import deps
import datetime
from app.schemas.evaluation import (
    EvaluationWeight,
    EvaluationWeightCreate,
    PeerEvaluationCreate,
    PmEvaluationCreate,
    QualitativeEvaluationCreate,
    FinalEvaluation,
    FinalEvaluationCalculateRequest,
    EvaluationPeriod,
    EvaluationPeriodCreate,
    DepartmentGradeRatio,
    DepartmentGradeRatioCreate,
    GradeAdjustmentRequest,
)
from app.models.user import User as UserModel, UserRole
from app.crud import grade_adjustment, crud_report
from app.exceptions import GradeAdjustmentError, GradeTOExceededError

router = APIRouter()

@router.post(
    "/adjust-grades",
    response_model=List[FinalEvaluation],
    dependencies=[Depends(deps.get_current_user)],
)
def adjust_grades(
    *,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
    adjustments_in: GradeAdjustmentRequest,
) -> Any:
    """
    Adjust final grades for users.
    - Accessible only by DEPT_HEAD or ADMIN.
    - DEPT_HEAD can only adjust grades for users in their own department.
    - The number of B+ and B- grades must be equal within a department.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.DEPT_HEAD]:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges for this operation",
        )

    if current_user.role == UserRole.ADMIN:
        # Admins could in theory adjust for any department, but the logic is
        # scoped to a single department for B+/B- validation. The first user's
        # department is used as the target.
        if not adjustments_in.adjustments:
            return []
        first_user = crud.user.user.get(db, id=adjustments_in.adjustments[0].user_id)
        if not first_user or not first_user.organization_id:
            raise HTTPException(status_code=400, detail="Cannot determine department for adjustment.")
        department_id = first_user.organization_id
    else: # DEPT_HEAD
        if not current_user.organization_id:
            raise HTTPException(status_code=400, detail="User does not belong to a department.")
        department_id = current_user.organization_id

    try:
        updated_evaluations = grade_adjustment.adjust_grades_for_department(
            db=db,
            department_id=department_id,
            evaluation_period=adjustments_in.evaluation_period,
            adjustments=adjustments_in.adjustments,
            current_user_role=current_user.role,
        )
        return updated_evaluations
    except GradeAdjustmentError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except GradeTOExceededError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


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

MAX_SCORES = [20, 20, 10, 10, 10, 10, 20]

@router.post("/peer-evaluations/", response_model=List[schemas.PeerEvaluation])
def create_or_update_peer_evaluations(
    *,
    db: Session = Depends(deps.get_db),
    evaluations_in: schemas.PeerEvaluationCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create or update peer evaluations for a user.
    """
    active_period = crud.evaluation_period.get_active_period(db)
    if not active_period:
        raise HTTPException(status_code=400, detail="No active evaluation period.")

    if evaluations_in.evaluations:
        total_score_sum = 0
        for e in evaluations_in.evaluations:
            if len(e.scores) != 7:
                raise HTTPException(
                    status_code=400,
                    detail=f"Evaluation for evaluatee {e.evaluatee_id} must have exactly 7 scores.",
                )
            
            for i, score in enumerate(e.scores):
                if not 0 <= score <= MAX_SCORES[i]:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Score at index {i} for evaluatee {e.evaluatee_id} is out of range (0-{MAX_SCORES[i]}).",
                    )
            
            total_score_sum += sum(e.scores)

        # FR-A-3.1: The average of the scores given cannot exceed 70.
        if len(evaluations_in.evaluations) > 0 and (total_score_sum / len(evaluations_in.evaluations)) > 70:
            raise HTTPException(
                status_code=400,
                detail="Average score cannot exceed 70.",
            )

    # TODO: Add more validation
    # - Check if the evaluator and evaluatee are in the same project.

    return crud.peer_evaluation.peer_evaluation.upsert_multi(
        db,
        evaluations=evaluations_in.evaluations,
        evaluator_id=current_user.id,
        evaluation_period=active_period.name,
    )

@router.post("/pm-evaluations/", response_model=List[schemas.PmEvaluation])
def create_or_update_pm_evaluations(
    *,
    db: Session = Depends(deps.get_db),
    evaluations_in: schemas.PmEvaluationCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create or update PM evaluations for project members.
    """
    active_period = crud.evaluation_period.get_active_period(db)
    if not active_period:
        raise HTTPException(status_code=400, detail="No active evaluation period.")

    if not evaluations_in.evaluations:
        return []

    # Validate all projects first
    project_ids = {e.project_id for e in evaluations_in.evaluations}
    for project_id in project_ids:
        project_member = crud.project_member.project_member.get_by_user_and_project(
            db, user_id=current_user.id, project_id=project_id
        )
        if not project_member or not project_member.is_pm:
            raise HTTPException(
                status_code=403,
                detail=f"User is not a Project Manager for project {project_id}.",
            )

    for evaluation in evaluations_in.evaluations:
        # Check if the score is valid
        if not 0 <= evaluation.score <= 100:
            raise HTTPException(
                status_code=400,
                detail="Score must be between 0 and 100.",
            )

    return crud.pm_evaluation.pm_evaluation.upsert_multi(
        db,
        evaluations=evaluations_in.evaluations,
        evaluator_id=current_user.id,
        evaluation_period=active_period.name,
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
    active_period = crud.evaluation_period.get_active_period(db)
    if not active_period:
        raise HTTPException(status_code=400, detail="No active evaluation period.")

    # FR-A-3.5: Team lead/Dept head can evaluate their members.
    if current_user.role not in [UserRole.TEAM_LEAD, UserRole.DEPT_HEAD]:
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

    return crud.qualitative_evaluation.qualitative_evaluation.create_multi(
        db,
        evaluations=evaluations_in.evaluations,
        evaluator_id=current_user.id,
        evaluation_period=active_period.name,
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



@router.get("/pm-evaluations/{project_id}", response_model=schemas.PmEvaluationDetail)
def read_pm_evaluation_details(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get details for a PM to conduct evaluations for a specific project.
    """
    active_period = crud.evaluation_period.get_active_period(db)
    if not active_period:
        raise HTTPException(status_code=400, detail="No active evaluation period.")

    project = crud.project.project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    # Check if the current user is a PM for this project
    project_member_pm = crud.project_member.project_member.get_by_user_and_project(
        db, user_id=current_user.id, project_id=project_id
    )
    if not project_member_pm or not project_member_pm.is_pm:
        raise HTTPException(
            status_code=403,
            detail="User is not a Project Manager for this project.",
        )

    project_members = crud.project_member.project_member.get_multi_by_project_with_user_details(
        db, project_id=project_id
    )
    
    members_to_evaluate = []
    evaluated_count = 0
    for member in project_members:
        if member.user_id == current_user.id:
            continue

        existing_eval = crud.pm_evaluation.pm_evaluation.get_by_evaluator_and_evaluatee(
            db,
            project_id=project_id,
            evaluator_id=current_user.id,
            evaluatee_id=member.user_id,
            evaluation_period=active_period.name,
        )

        target = schemas.PmEvaluationTarget(
            evaluatee_id=member.user_id,
            evaluatee_name=member.full_name,
            score=existing_eval.score if existing_eval else None,
            comment=existing_eval.comment if existing_eval else None,
        )
        members_to_evaluate.append(target)
        if existing_eval:
            evaluated_count += 1

    status = "NOT_STARTED"
    if evaluated_count > 0:
        status = "IN_PROGRESS"
    if evaluated_count == len(members_to_evaluate) and evaluated_count > 0:
        status = "COMPLETED"

    return schemas.PmEvaluationDetail(
        project_id=project.id,
        project_name=project.name,
        status=status,
        members_to_evaluate=members_to_evaluate,
    )


@router.get("/peer-evaluations/{project_id}", response_model=schemas.PeerEvaluationDetail)
def read_peer_evaluation_details(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get details for conducting a peer evaluation for a specific project.
    """
    active_period = crud.evaluation_period.get_active_period(db)
    if not active_period:
        raise HTTPException(status_code=400, detail="No active evaluation period.")

    project = crud.project.project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    project_members = crud.project_member.project_member.get_multi_by_project_with_user_details(
        db, project_id=project_id
    )
    
    peers_to_evaluate = []
    evaluated_count = 0
    for member in project_members:
        if member.user_id == current_user.id:
            continue

        existing_eval = crud.peer_evaluation.peer_evaluation.get_by_evaluator_and_evaluatee(
            db,
            project_id=project_id,
            evaluator_id=current_user.id,
            evaluatee_id=member.user_id,
            evaluation_period=active_period.name,
        )

        target = schemas.PeerEvaluationTarget(
            evaluatee_id=member.user_id,
            evaluatee_name=member.full_name,
            scores=existing_eval.scores if existing_eval else [],
            comment=existing_eval.comment if existing_eval else None,
        )
        peers_to_evaluate.append(target)
        if existing_eval:
            evaluated_count += 1

    status = "NOT_STARTED"
    if evaluated_count > 0:
        status = "IN_PROGRESS"
    if evaluated_count == len(peers_to_evaluate) and evaluated_count > 0:
        status = "COMPLETED"

    return schemas.PeerEvaluationDetail(
        project_id=project.id,
        project_name=project.name,
        status=status,
        peers_to_evaluate=peers_to_evaluate,
    )


@router.get("/my-tasks", response_model=List[schemas.MyEvaluationTask])
def my_evaluation_tasks(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get all projects the current user needs to evaluate in the active period.
    """
    active_period = crud.evaluation_period.get_active_period(db)
    if not active_period:
        return []

    project_memberships = crud.project_member.project_member.get_multi_by_user_and_period(
        db,
        user_id=current_user.id,
        start_date=active_period.start_date,
        end_date=active_period.end_date,
    )

    tasks = []
    for pm in project_memberships:
        if pm.project:
            tasks.append(
                schemas.MyEvaluationTask(
                    project_id=pm.project_id,
                    project_name=pm.project.name,
                    user_role_in_project="PM" if pm.is_pm else "MEMBER",
                )
            )
    return tasks


@router.get("/me", response_model=schemas.MyEvaluationResult)
def read_my_evaluation_result(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    evaluation_period: Optional[str] = None,
) -> Any:
    """
    Retrieve the current user's own evaluation results.
    """
    # Determine the evaluation period if not provided
    if not evaluation_period:
        today = datetime.date.today()
        evaluation_period = f"{today.year}-H{1 if today.month <= 6 else 2}"

    period = crud.evaluation_period.get_by_name(db, name=evaluation_period)
    if not period:
        raise HTTPException(
            status_code=404,
            detail=f"Evaluation period '{evaluation_period}' not found.",
        )

    # FR-A-5.1: Can view final grade and PM scores
    final_eval = crud.final_evaluation.get_by_user_and_period(
        db, evaluatee_id=current_user.id, period_id=period.id
    )
    pm_scores_data = crud.pm_evaluation.pm_evaluation.get_for_evaluatee_by_period(
        db, evaluatee_id=current_user.id, evaluation_period=evaluation_period
    )

    pm_scores = [
        schemas.PmScoreResult(
            project_name=score.project_name,
            pm_name=score.pm_name,
            score=score.score,
        )
        for score in pm_scores_data
    ]

    return schemas.MyEvaluationResult(
        evaluation_period=evaluation_period,
        grade=final_eval.grade if final_eval else None,
        pm_scores=pm_scores,
    )


@router.get("/{user_id}/result", response_model=schemas.ManagerEvaluationView)
def read_subordinate_evaluation_result(
    *,
    db: Session = Depends(deps.get_db),
    user_to_view: models.User = Depends(deps.get_user_as_subordinate),
    evaluation_period: Optional[str] = None,
) -> Any:
    """
    Retrieve a subordinate's full evaluation result.
    Accessible by DEPT_HEAD for their subordinates, and ADMIN for anyone.
    """
    if not evaluation_period:
        today = datetime.date.today()
        evaluation_period = f"{today.year}-H{1 if today.month <= 6 else 2}"

    period = crud.evaluation_period.get_by_name(db, name=evaluation_period)
    if not period:
        raise HTTPException(
            status_code=404,
            detail=f"Evaluation period '{evaluation_period}' not found.",
        )

    # FR-A-5.3: Can view all scores, rank, and anonymous feedback
    final_eval = crud.final_evaluation.get_by_user_and_period(
        db, evaluatee_id=user_to_view.id, period_id=period.id
    )
    if not final_eval:
        raise HTTPException(
            status_code=404,
            detail="Final evaluation not found for this user and period.",
        )

    feedback_rows = crud.peer_evaluation.peer_evaluation.get_feedback_for_evaluatee_by_period(
        db, evaluatee_id=user_to_view.id, evaluation_period=evaluation_period
    )
    # The query returns tuples, so we extract the first element
    peer_feedback = [item[0] for item in feedback_rows]

    return schemas.ManagerEvaluationView(
        final_evaluation=final_eval,
        peer_feedback=peer_feedback,
    )



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

    if current_user.role not in [UserRole.DEPT_HEAD, UserRole.ADMIN]:
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
        if current_user.role == UserRole.DEPT_HEAD:
            # Calculate for all subordinates of the current DEPT_HEAD
            target_users = crud.user.user.get_subordinates(db, user_id=current_user.id)
        elif current_user.role == UserRole.ADMIN:
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
    current_user: models.User = Depends(deps.get_current_admin_or_dept_head_user),
) -> Any:
    """
    Retrieve evaluation periods. (Admin only)
    """
    evaluation_periods = crud.evaluation_period.get_multi(db, skip=skip, limit=limit)
    today = datetime.date.today()
    
    response_periods = []
    for period in evaluation_periods:
        is_active = period.start_date <= today <= period.end_date
        response_periods.append(
            schemas.EvaluationPeriod(
                id=period.id,
                name=period.name,
                start_date=period.start_date,
                end_date=period.end_date,
                is_active=is_active,
            )
        )
    return response_periods


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


# New endpoints for evaluation UX improvement

@router.get("/periods/{period_id}/evaluated-users", response_model=List[schemas.report.EvaluatedUser])
def read_evaluated_users_by_period(
    *,
    db: Session = Depends(deps.get_db),
    period_id: int,
    current_user: models.User = Depends(deps.get_current_admin_or_dept_head_user),
) -> Any:
    """
    Get a list of users for whom final evaluations have been completed for a specific period.
    - Accessible by ADMIN and DEPT_HEAD.
    - DEPT_HEAD will only see users from their own department.
    """
    users = crud_report.get_evaluated_users_by_period(
        db, period_id=period_id, current_user=current_user
    )
    return users


@router.get("/periods/{period_id}/users/{user_id}/details", response_model=schemas.report.DetailedEvaluationResult)
def read_detailed_evaluation_result(
    *,
    db: Session = Depends(deps.get_db),
    period_id: int,
    user_id: int,
    current_user: models.User = Depends(deps.get_current_user), # First, get the current user
) -> Any:
    """
    Get the detailed evaluation result for a specific user and period.
    - Accessible by ADMIN for any user.
    - Accessible by DEPT_HEAD for their subordinates only.
    """
    # Check for authorization
    if current_user.role == UserRole.ADMIN:
        pass  # Admin can view anyone
    elif current_user.role == UserRole.DEPT_HEAD:
        subordinate_ids = {user.id for user in crud.user.user.get_subordinates(db, user_id=current_user.id)}
        if user_id not in subordinate_ids:
            raise HTTPException(status_code=403, detail="Not enough privileges to view this user's evaluation")
    else:
        raise HTTPException(status_code=403, detail="Not enough privileges for this operation")

    result = crud_report.get_detailed_evaluation_result(db, period_id=period_id, user_id=user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User or evaluation period not found")
    
    return result
