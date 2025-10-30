from pydantic import BaseModel
from typing import Optional, List, Literal

from app.schemas.strength import StrengthProfile
from app.schemas.user import UserInfo


class GrowthAndCultureReport(BaseModel):
    """
    FR-A-4.6: Growth & Culture 리포트 조회를 위한 스키마.
    관리자가 정성평가, 등급 조정, 동점자 처리 수행 시 참고 자료로 조회합니다.
    """
    strength_profile: StrengthProfile
    collaboration_summary: Optional[dict] = None  # FR-B-2.4, 추후 구현


# API: /api/v1/evaluations/periods/{period_id}/evaluated-users
class EvaluatedUser(UserInfo):
    """특정 평가 기간에 평가가 완료된 사용자 목록 조회를 위한 스키마"""
    pass


# API: /api/v1/evaluations/periods/{period_id}/users/{user_id}/details
class FinalEvaluationDetail(BaseModel):
    grade: Optional[str] = None
    final_score: Optional[float] = None


class ProjectEvaluationDetail(BaseModel):
    project_id: int
    project_name: str
    participation_weight: int
    peer_evaluation_score: Optional[float] = None
    pm_evaluation_score: Optional[float] = None
    peer_feedback: List[str] = []


class QualitativeEvaluationDetail(BaseModel):
    score: Optional[float] = None
    comment: Optional[str] = None


class DetailedEvaluationResult(BaseModel):
    status: Literal["COMPLETED", "IN_PROGRESS"]
    user_info: UserInfo
    final_evaluation: Optional[FinalEvaluationDetail] = None
    project_evaluations: List[ProjectEvaluationDetail] = []
    qualitative_evaluation: Optional[QualitativeEvaluationDetail] = None
