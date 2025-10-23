from pydantic import BaseModel
from typing import Optional

from app.schemas.strength import StrengthProfile


class GrowthAndCultureReport(BaseModel):
    """
    FR-A-4.6: Growth & Culture 리포트 조회를 위한 스키마.
    관리자가 정성평가, 등급 조정, 동점자 처리 수행 시 참고 자료로 조회합니다.
    """
    strength_profile: StrengthProfile
    collaboration_summary: Optional[dict] = None  # FR-B-2.4, 추후 구현
