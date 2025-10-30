from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, models, schemas
from app.models.user import UserRole


def get_evaluated_users_by_period(
    db: Session, *, period_id: int, current_user: models.User
) -> List[schemas.report.EvaluatedUser]:
    """
    특정 평가 기간에 대해 최종 평가가 완료된 사용자 목록을 조회합니다.
    - DEPT_HEAD: 자신의 하위 조직에 속한 사용자만 조회합니다.
    - ADMIN: 모든 사용자를 조회합니다.
    """
    period = crud.evaluation_period.get(db, id=period_id)
    if not period:
        return []

    # 먼저 해당 기간에 최종 평가가 생성된 모든 사용자 ID를 가져옵니다.
    query = (
        db.query(models.FinalEvaluation.evaluatee_id)
        .filter(models.FinalEvaluation.evaluation_period == period.name)
    )
    
    evaluated_user_ids = {item[0] for item in query.all()}

    if not evaluated_user_ids:
        return []

    # 역할에 따라 필터링할 사용자 목록을 결정합니다.
    if current_user.role == UserRole.ADMIN:
        # ADMIN은 평가받은 모든 사용자를 대상으로 합니다.
        target_user_ids = evaluated_user_ids
    elif current_user.role == UserRole.DEPT_HEAD:
        # DEPT_HEAD는 자신의 하위 조직원 중에서 평가받은 사용자만 대상으로 합니다.
        subordinate_ids = {
            user.id for user in crud.user.user.get_subordinates(db, user_id=current_user.id)
        }
        target_user_ids = evaluated_user_ids.intersection(subordinate_ids)
    else:
        # 그 외 역할은 조회 권한이 없습니다. (API 레벨에서 차단되지만 안전장치)
        return []

    if not target_user_ids:
        return []

    # 최종 대상 사용자들의 상세 정보를 조회합니다.
    users = db.query(models.User).filter(models.User.id.in_(list(target_user_ids))).all()

    # 스키마에 맞게 변환하여 반환합니다.
    return [
        schemas.report.EvaluatedUser(
            user_id=user.id,
            full_name=user.full_name,
            title=user.title,
            organization_name=user.organization.name if user.organization else None,
        )
        for user in users
    ]


def get_detailed_evaluation_result(
    db: Session, *, period_id: int, user_id: int
) -> Optional[schemas.report.DetailedEvaluationResult]:
    """
    특정 사용자의 상세 평가 결과를 조회합니다.
    - 평가가 완료되었으면 모든 상세 내역을 포함하여 반환합니다.
    - 평가가 진행 중이면 상태와 기본 정보만 반환합니다.
    """
    user = crud.user.user.get(db, id=user_id)
    if not user:
        return None

    user_info = schemas.user.UserInfo(
        user_id=user.id,
        full_name=user.full_name,
        title=user.title,
        organization_name=user.organization.name if user.organization else None,
    )

    final_eval = crud.final_evaluation.get_by_user_and_period(
        db, evaluatee_id=user_id, period_id=period_id
    )

    if not final_eval:
        return schemas.report.DetailedEvaluationResult(
            status="IN_PROGRESS",
            user_info=user_info,
        )

    # Project Evaluations
    project_evaluations = []
    project_members = crud.project_member.project_member.get_multi_by_user_and_evaluation_period(
        db, user_id=user_id, evaluation_period_id=period_id
    )

    for pm in project_members:
        if not pm.project:
            continue

        # Peer Evaluation
        peer_score = crud.peer_evaluation.peer_evaluation.get_average_score_for_evaluatee(
            db, evaluatee_id=user_id, project_id=pm.project_id, period_id=period_id
        )
        peer_feedback = crud.peer_evaluation.peer_evaluation.get_feedback_for_evaluatee(
            db, evaluatee_id=user_id, project_id=pm.project_id, period_id=period_id
        )

        # PM Evaluation
        pm_eval = crud.pm_evaluation.pm_evaluation.get_for_evaluatee_by_project_and_period(
            db, evaluatee_id=user_id, project_id=pm.project_id, period_id=period_id
        )

        project_eval_detail = schemas.report.ProjectEvaluationDetail(
            project_id=pm.project_id,
            project_name=pm.project.name,
            participation_weight=pm.participation_weight,
            peer_evaluation_score=peer_score,
            pm_evaluation_score=pm_eval.score if pm_eval else None,
            peer_feedback=[f.comment for f in peer_feedback if f.comment],
        )
        project_evaluations.append(project_eval_detail)

    # Qualitative Evaluation
    qualitative_eval = crud.qualitative_evaluation.qualitative_evaluation.get_by_evaluatee_and_period(
        db, evaluatee_id=user_id, period_id=period_id
    )

    return schemas.report.DetailedEvaluationResult(
        status="COMPLETED",
        user_info=user_info,
        final_evaluation=schemas.report.FinalEvaluationDetail(
            grade=final_eval.grade,
            final_score=final_eval.final_score,
        ),
        project_evaluations=project_evaluations,
        qualitative_evaluation=schemas.report.QualitativeEvaluationDetail(
            score=qualitative_eval.score if qualitative_eval else None,
            comment=qualitative_eval.comment if qualitative_eval else None,
        ),
    )
