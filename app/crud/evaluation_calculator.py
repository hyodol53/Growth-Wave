from sqlalchemy.orm import Session
from app import crud, models, schemas
from statistics import mean

def calculate_and_store_final_scores(
    db: Session, *, evaluatee: models.User, evaluation_period: str
) -> models.FinalEvaluation | None:
    """
    Calculates and stores the final evaluation score for a given user and period
    based on the new 70/30 project/qualitative weighting.
    """
    period = crud.evaluation_period.get_by_name(db, name=evaluation_period)
    if not period:
        return None

    # 1. Get evaluation weights for the user's role
    #role_weights = crud.evaluation.evaluation_weight.get_multi_by_role(db, role=evaluatee.role)
    #if not role_weights:
        #return None
    
    #weight_map = {item.item: item.weight for item in role_weights}
    
    # 2. Get user's project memberships
    project_memberships = crud.project_member.project_member.get_multi_by_user(db, user_id=evaluatee.id)
    
    total_weighted_peer_score = 0
    total_weighted_pm_score = 0

    is_pm_role = evaluatee.role in [models.UserRole.TEAM_LEAD, models.UserRole.DEPT_HEAD]

    # 3. Calculate weighted average score from all projects
    if is_pm_role:
        pm_evals = crud.pm_evaluation.pm_evaluation.get_by_evaluatee(
            db, evaluatee_id=evaluatee.id, evaluation_period=evaluation_period
        )
        total_weighted_pm_score = pm_evals[0].score if pm_evals else 0
        if project_memberships:
            for membership in project_memberships:
                project_weight = membership.participation_weight / 100.0
                avg_peer_score = crud.peer_evaluation.peer_evaluation.get_average_score_for_evaluatee(
                    db, project_id=membership.project_id, evaluatee_id=evaluatee.id, period_id=period.id
                )
                if avg_peer_score:
                    total_weighted_peer_score += avg_peer_score * project_weight
    else:
        if project_memberships:
            for membership in project_memberships:
                project_weight = membership.participation_weight / 100.0
                avg_peer_score = crud.peer_evaluation.peer_evaluation.get_average_score_for_evaluatee(
                    db, project_id=membership.project_id, evaluatee_id=evaluatee.id, period_id=period.id
                )
                if avg_peer_score:
                    total_weighted_peer_score += avg_peer_score * project_weight
                pm_eval = crud.pm_evaluation.pm_evaluation.get_for_evaluatee_by_project_and_period(
                    db, project_id=membership.project_id, evaluatee_id=evaluatee.id, period_id=period.id
                )
                if pm_eval:
                    total_weighted_pm_score += pm_eval.score * project_weight
    
    # 4. Calculate the combined project score component
    #peer_weight = weight_map.get(models.evaluation.EvaluationItem.PEER_REVIEW, 0)
    #pm_weight = weight_map.get(models.evaluation.EvaluationItem.PM_REVIEW, 0)
    peer_weight = 50
    pm_weight = 50
    
    project_score = 0
    # Normalize weights within the project score component
    if (peer_weight + pm_weight) > 0:
        normalized_peer_weight = peer_weight / (peer_weight + pm_weight)
        normalized_pm_weight = pm_weight / (peer_weight + pm_weight)
        project_score = (total_weighted_peer_score * normalized_peer_weight) + \
                        (total_weighted_pm_score * normalized_pm_weight)

    # 5. Get qualitative evaluation score
    qualitative_eval = crud.qualitative_evaluation.qualitative_evaluation.get_by_evaluatee_and_period(
        db, evaluatee_id=evaluatee.id, period_id=period.id
    )
    
    qualitative_combined_score = 0
    if qualitative_eval:
        qualitative_combined_score = (
            qualitative_eval.qualitative_score + qualitative_eval.department_contribution_score
        )
    
    # 6. Calculate final score using the 70/30 split
    # Normalize qualitative score (out of 30) to a 100-point scale
    qualitative_normalized_score = (qualitative_combined_score / 30.0) * 100
    
    final_score = (project_score * 0.7) + (qualitative_normalized_score * 0.3)
    
    # 7. Create and store the final evaluation record
    final_eval_in = schemas.FinalEvaluationCreate(
        evaluatee_id=evaluatee.id,
        evaluation_period=evaluation_period,
        peer_score=total_weighted_peer_score,
        pm_score=total_weighted_pm_score,
        qualitative_score=qualitative_combined_score, # Store the combined score
        final_score=final_score,
    )
    
    db_obj = crud.final_evaluation.get_by_user_and_period(
        db, evaluatee_id=evaluatee.id, period_id=period.id
    )
    if db_obj:
        final_evaluation = crud.final_evaluation.update(db, db_obj=db_obj, obj_in=final_eval_in)
    else:
        final_evaluation = crud.final_evaluation.create(db, obj_in=final_eval_in)

    return final_evaluation


def calculate_scores_for_period(db: Session, *, period_id: int) -> bool:
    """
    Calculates final scores for all users for a given evaluation period.
    """
    period = crud.evaluation_period.get(db, id=period_id)
    if not period:
        return False

    users = crud.user.user.get_multi(db)
    for user in users:
        calculate_and_store_final_scores(
            db, evaluatee=user, evaluation_period=period.name
        )
    
    return True