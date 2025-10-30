# API: 특정 사용자의 상세 평가 결과 조회

## `GET /api/v1/evaluations/periods/{period_id}/users/{user_id}/details`

### 1. 개요

특정 평가 기간(`period_id`)과 특정 사용자(`user_id`)에 대한 모든 상세 평가 내역을 조회합니다. 기존의 최종 등급뿐만 아니라, 해당 기간의 프로젝트별 평가 내역, 정성 평가 결과 등을 모두 포함하여 반환합니다.

### 2. 접근 권한

-   `DEPT_HEAD` (실장): 자신의 하위 조직원에 대해서만 조회 가능
-   `ADMIN` (관리자): 모든 사용자에 대해 조회 가능

### 3. 요청 (Request)

#### 3.1. 경로 파라미터 (Path Parameters)

| 이름 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `period_id` | `integer` | Y | 조회할 평가 기간의 ID |
| `user_id` | `integer` | Y | 조회할 사용자의 ID |

#### 3.2. 헤더 (Headers)

| 이름 | 값 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `Authorization` | `Bearer <JWT_TOKEN>` | Y | 사용자의 JWT Access Token |

### 4. 응답 (Response)

#### 4.1. 성공 (200 OK) - 평가 완료 시

**Content-Type:** `application/json`

```json
{
  "status": "COMPLETED",
  "user_info": {
    "user_id": 1,
    "full_name": "김직원",
    "title": "선임연구원",
    "organization_name": "플랫폼개발팀"
  },
  "final_evaluation": {
    "grade": "A",
    "final_score": 92.5
  },
  "project_evaluations": [
    {
      "project_id": 101,
      "project_name": "Growth-Wave 개발",
      "participation_weight": 60,
      "peer_evaluation_score": 85.0,
      "pm_evaluation_score": 95.0,
      "peer_feedback": [
        "협업에 매우 적극적이었습니다.",
        "꼼꼼하게 리뷰해주셔서 감사합니다."
      ]
    },
    {
      "project_id": 102,
      "project_name": "신규 서비스 기획",
      "participation_weight": 40,
      "peer_evaluation_score": 78.0,
      "pm_evaluation_score": 90.0,
      "peer_feedback": []
    }
  ],
  "qualitative_evaluation": {
    "score": 90.0,
    "comment": "팀에 대한 기여도가 높고 성실함."
  }
}
```

#### 4.2. 성공 (200 OK) - 평가 미완료 시

**Content-Type:** `application/json`

-   `FinalEvaluation` 레코드가 존재하지 않을 경우, `status`를 `IN_PROGRESS`로 설정하고 나머지 데이터는 `null` 또는 빈 배열로 반환합니다.

```json
{
  "status": "IN_PROGRESS",
  "user_info": {
    "user_id": 2,
    "full_name": "이직원",
    "title": "연구원",
    "organization_name": "플랫폼개발팀"
  },
  "final_evaluation": null,
  "project_evaluations": [],
  "qualitative_evaluation": null
}
```

#### 4.3. 실패 (Failure)

-   **401 Unauthorized**: 인증 토큰이 유효하지 않은 경우
-   **403 Forbidden**: 조회 권한이 없는 경우 (예: 실장이 다른 부서의 직원을 조회)
-   **404 Not Found**: `period_id` 또는 `user_id`에 해당하는 데이터가 존재하지 않는 경우
