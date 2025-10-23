from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.user import UserRole

router = APIRouter()


@router.get("/users/{user_id}/growth-culture-report", response_model=schemas.GrowthAndCultureReport)
def get_growth_culture_report(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    FR-A-4.6: Growth & Culture 리포트 조회.

    - **Access**: DEPT_HEAD, ADMIN, 또는 그 이상의 권한 필요.
    - DEPT_HEAD는 자신의 하위 조직원에 대한 리포트만 조회 가능.
    """
    # 권한 확인: 관리자 또는 실장급 이상만 접근 가능
    if current_user.role not in [UserRole.ADMIN, UserRole.DEPT_HEAD]:
        raise HTTPException(
            status_code=403, detail="You do not have enough privileges for this operation."
        )

    # 대상 사용자 조회
    target_user = crud.user.user.get(db, id=user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 실장의 경우, 자신의 하위 조직원인지 확인
    if current_user.role == UserRole.DEPT_HEAD:
        # Get all descendant organization IDs
        descendant_orgs = crud.organization.get_all_descendant_orgs(db, org_id=current_user.organization_id)
        allowed_org_ids = {org.id for org in descendant_orgs}
        allowed_org_ids.add(current_user.organization_id)

        if target_user.organization_id not in allowed_org_ids:
            raise HTTPException(
                status_code=403, detail="You can only view reports for users in your department."
            )

    # 데이터 조회 (Strength Profile)
    strength_stats = crud.praise.get_strength_profile_for_user(db, user=target_user)
    total_praises = len(target_user.praises_received)
    strength_profile = schemas.StrengthProfile(
        user_id=target_user.id,
        full_name=target_user.full_name,
        total_praises=total_praises,
        strengths=strength_stats
    )

    # 리포트 생성 및 반환
    return schemas.GrowthAndCultureReport(
        strength_profile=strength_profile,
        collaboration_summary={"message": "This feature will be implemented in the future."}
    )
