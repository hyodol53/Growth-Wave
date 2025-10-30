from sqlalchemy.orm import Session
from app import crud, models, schemas
from statistics import mean

def calculate_and_store_final_scores(
    db: Session, *, evaluatee: models.User, evaluation_period: str
) -> models.FinalEvaluation:
    """
    Calculates and stores the final evaluation score for a given user and period.
    """
    period = crud.evaluation_period.get_by_name(db, name=evaluation_period)
    if not period:
        return None

    # 1. Get evaluation weights for the user's role
    role_weights = crud.evaluation.evaluation_weight.get_multi_by_role(db, role=evaluatee.role)
    if not role_weights:
        return None 
    
    weight_map = {item.item: item.weight for item in role_weights}
    
    # 2. Get user's project memberships and participation weights
    project_memberships = crud.project_member.project_member.get_multi_by_user(db, user_id=evaluatee.id)
    
    total_weighted_peer_score = 0
    total_weighted_pm_score = 0

    # Check if the evaluatee is a PM (TEAM_LEAD or DEPT_HEAD)
    is_pm_role = evaluatee.role in [models.UserRole.TEAM_LEAD, models.UserRole.DEPT_HEAD]

    # 3 & 4. Calculate weighted average score from all projects
    if is_pm_role:
        # For PMs, get the single score entered by an admin (FR-A-3.4)
        # Assuming there is one such evaluation for the period.
        # We take the first one found.
        pm_evals = crud.pm_evaluation.pm_evaluation.get_by_evaluatee(
            db, evaluatee_id=evaluatee.id, evaluation_period=evaluation_period
        )
        total_weighted_pm_score = pm_evals[0].score if pm_evals else 0

        # Peer score for PMs might need special handling, but for now, we calculate it as usual.
        if project_memberships:
            for membership in project_memberships:
                project_weight = membership.participation_weight / 100.0
                avg_peer_score = crud.peer_evaluation.peer_evaluation.get_average_score_for_evaluatee(
                    db, project_id=membership.project_id, evaluatee_id=evaluatee.id, period_id=period.id
                )
                if avg_peer_score:
                    total_weighted_peer_score += avg_peer_score * project_weight
    else:
        # For non-PMs, calculate as before
        if project_memberships:
            for membership in project_memberships:
                project_weight = membership.participation_weight / 100.0
        
                # Peer evaluations for the project
                avg_peer_score = crud.peer_evaluation.peer_evaluation.get_average_score_for_evaluatee(
                    db, project_id=membership.project_id, evaluatee_id=evaluatee.id, period_id=period.id
                )
                if avg_peer_score:
                    total_weighted_peer_score += avg_peer_score * project_weight
        
                # PM evaluations for the project
                pm_eval = crud.pm_evaluation.pm_evaluation.get_for_evaluatee_by_project_and_period(
                    db, project_id=membership.project_id, evaluatee_id=evaluatee.id, period_id=period.id
                )
                if pm_eval:
                    total_weighted_pm_score += pm_eval.score * project_weight
    
    # 5. Get qualitative evaluation score
    qualitative_eval = crud.qualitative_evaluation.qualitative_evaluation.get_by_evaluatee_and_period(
        db, evaluatee_id=evaluatee.id, period_id=period.id
    )
    qualitative_score = qualitative_eval.score if qualitative_eval else 0
    
    # 6. Calculate final score using weights
    final_score = (
        total_weighted_peer_score * (weight_map.get(models.evaluation.EvaluationItem.PEER_REVIEW, 0) / 100.0) +
        total_weighted_pm_score * (weight_map.get(models.evaluation.EvaluationItem.PM_REVIEW, 0) / 100.0) +
        qualitative_score * (weight_map.get(models.evaluation.EvaluationItem.QUALITATIVE_REVIEW, 0) / 100.0)
    )
    
    # 7. Create and store the final evaluation record
    final_eval_in = schemas.FinalEvaluationCreate(
        evaluatee_id=evaluatee.id,
        evaluation_period=evaluation_period,
        peer_score=total_weighted_peer_score,
        pm_score=total_weighted_pm_score,
        qualitative_score=qualitative_score,
        final_score=final_score,
    )
    
    # Check if a final evaluation already exists and update it, or create a new one
    db_obj = crud.final_evaluation.get_by_user_and_period(
        db, evaluatee_id=evaluatee.id, period_id=period.id
    )
    if db_obj:
        final_evaluation = crud.final_evaluation.update(db, db_obj=db_obj, obj_in=final_eval_in)
    else:
        final_evaluation = crud.final_evaluation.create(db, obj_in=final_eval_in)

    return final_evaluation