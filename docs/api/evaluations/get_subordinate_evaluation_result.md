# GET /api/v1/evaluations/{user_id}/result

## API 설명
실장(`DEPT_HEAD`) 또는 시스템 관리자(`ADMIN`)가 특정 사용자(주로 하위 직원)의 상세 평가 결과를 조회합니다.

이 API는 요구사항 `FR-A-5.3`을 충족하며, 관리자는 소속원의 모든 점수, 석차, 익명 피드백 등을 열람할 수 있습니다.

## 접근 권한
- **`DEPT_HEAD`**: 자신이 속한 부서 및 모든 하위 부서의 구성원 정보만 조회할 수 있습니다.
- **`ADMIN`**: 시스템의 모든 사용자 정보를 조회할 수 있습니다.

## 요청 (Request)

### URL
`GET /api/v1/evaluations/{user_id}/result`

### 경로 파라미터 (Path Parameters)
- `user_id` (integer, required): 조회할 사용자의 ID

### 헤더 (Headers)
- `Authorization`: `Bearer <ACCESS_TOKEN>`

### 쿼리 파라미터 (Query Parameters)
- `evaluation_period` (string, optional): 조회할 평가 기간의 이름 (예: 2025-H1 , 2025-하반기 등). 지정하지 않으면 현재 날짜를 기준으로 자동으로 설정됩니다.

## 응답 (Response)

### 성공 (Success)
- **상태 코드:** `200 OK`
- **본문 (Body):** `ManagerEvaluationView` 스키마
```json
{
  "final_evaluation": {
    "evaluatee_id": 15,
    "evaluation_period": "2025-H1",
    "peer_score": 85.5,
    "pm_score": 90.0,
    "qualitative_score": 88.0,
    "final_score": 87.6,
    "grade": "S",
    "id": 101
  },
  "peer_feedback": [
    "프로젝트에 대한 기여도가 높습니다.",
    "항상 동료들을 먼저 생각하고 배려하는 모습이 인상적이었습니다."
  ]
}
```

### 실패 (Failure)
- **상태 코드:** `401 Unauthorized`
  - **원인:** 인증되지 않은 사용자의 요청
- **상태 코드:** `403 Forbidden`
  - **원인:** 조회 권한이 없는 경우 (예: 일반 직원이 다른 직원 조회, 실장이 다른 부서 직원 조회)
- **상태 코드:** `404 Not Found`
  - **원인:**
    - `user_id`에 해당하는 사용자가 존재하지 않는 경우
    - 해당 평가 기간에 대한 최종 평가 데이터가 존재하지 않는 경우
