# Task: 정성평가 UX 개편 및 역할 기반 평가 정책 적용

**문서 ID:** `task_refactor_qualitative_evaluation_ux`
**작성자:** 프론트엔드 에이전트
**상태:** 제안 (Proposed)

## 1. 개요

본 문서는 기존의 다이얼로그 기반 정성평가 UX를 프로젝트 평가와 동일한 그리드(Grid) 형태로 변경하고, 제출 내역 확인 및 수정 기능을 지원하기 위한 백엔드 변경 사항을 기술합니다. 또한, 평가자의 역할(팀장/실장)에 따라 평가 대상이 자동으로 필터링되는 새로운 정책을 적용합니다.

## 2. 변경 필요사항

### 2.1. 신규 API 엔드포인트 추가

정성평가 데이터를 조회하고, 기존에 제출된 내역을 가져오기 위한 새로운 API가 필요합니다.

- **엔드포인트:** `GET /api/v1/evaluations/qualitative-evaluations/`
- **핵심 기능:**
    1.  **데이터 조회:** 현재 로그인한 평가자가 평가해야 할 모든 대상자의 목록과, 각 대상자에 대해 이전에 제출했던 평가 내역(점수, 피드백)을 함께 반환합니다.
        - 만약 특정 대상자에 대해 평가를 아직 제출하지 않았다면, 점수 및 피드백 필드는 `null`로 반환되어야 합니다.
    2.  **역할 기반 필터링 (중요):** API는 요청을 보낸 사용자의 역할을 서버 사이드에서 확인하여, 아래 정책에 따라 최종 평가 대상 목록을 필터링한 후 응답해야 합니다.
        - **요청자가 `team_lead` (팀장)일 경우:** 해당 팀장의 모든 하위 구성원을 평가 대상으로 반환합니다.
        - **요청자가 `dept_head` (실장)일 경우:** 해당 실장의 하위 구성원 중 **`team_lead` (팀장) 직책을 가진 사람만**을 평가 대상으로 반환합니다.
        - 그 외 역할(예: `admin`, `employee`)의 사용자가 요청할 경우, 빈 목록(`[]`)을 반환합니다.

### 2.2. API 스키마 (Pydantic) 추가

`GET /api/v1/evaluations/qualitative-evaluations/` 엔드포인트가 반환할 새로운 데이터 스키마를 정의해야 합니다.

- **대상 파일:** `app/schemas/evaluation.py`
- **추가할 스키마 예시:**

  ```python
  from pydantic import BaseModel
  from typing import List, Optional
  
  # 개별 평가 대상의 정보를 담는 스키마
  class MemberToEvaluateQualitatively(BaseModel):
      evaluatee_id: int
      evaluatee_name: str
      title: str  # 직책
      organization_name: str # 소속 조직
  
      # 기제출된 평가 데이터 (없을 경우 null)
      qualitative_score: Optional[int] = None
      department_contribution_score: Optional[int] = None
      feedback: Optional[str] = None
  
  # 최종 API 응답 스키마
  class QualitativeEvaluationData(BaseModel):
      status: str # "NOT_STARTED", "IN_PROGRESS", "COMPLETED"
      members_to_evaluate: List[MemberToEvaluateQualitatively]
  ```

### 2.3. 기존 API 활용 방안

- **`POST /api/v1/evaluations/qualitative-evaluations/`**
- 기존의 정성평가 제출 API는 그대로 유지하며, **생성(Create)과 수정(Update)을 모두 처리**하는 `upsert` 로직으로 활용합니다. 프론트엔드에서는 그리드에 표시된 모든 평가 대상의 데이터를 이 API를 통해 한 번에 제출할 것입니다.

## 3. 영향 범위

- **API:** 정성평가 데이터 조회를 위한 신규 API(`GET`)가 필요합니다.
- **Frontend:** 신규 API를 사용하여 그리드 기반의 새로운 정성평가 UI를 개발할 예정입니다. 기존의 다이얼로그 기반 UI는 삭제됩니다.
- **Database:** 별도의 데이터베이스 모델 변경은 필요하지 않을 것으로 예상됩니다.
