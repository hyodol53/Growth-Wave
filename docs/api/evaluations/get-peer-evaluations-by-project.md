# `GET /api/v1/evaluations/peer-evaluations/{project_id}`

## 1. 개요

특정 프로젝트(`project_id`)에 대해, 현재 로그인한 사용자가 평가해야 할 동료 목록과 이미 제출한 평가 내용(점수, 코멘트)을 조회합니다. 프론트엔드에서 프로젝트 선택 시 동료 평가 그리드의 내용을 채우는 데 사용됩니다.

## 2. 요청

### 2.1. Path Parameters

| Key | Type | 설명 |
| :--- | :--- | :--- |
| `project_id` | `integer` | 조회할 프로젝트의 ID |

### 2.2. Headers

| Key | Value | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `Authorization` | `Bearer <JWT_TOKEN>` | O | 사용자의 JWT Access Token |

## 3. 응답

### 3.1. 성공 (200 OK)

**Content-Type:** `application/json`

```json
{
  "project_id": 1,
  "project_name": "Growth-Wave 개발",
  "status": "IN_PROGRESS",
  "peers_to_evaluate": [
    {
      "evaluatee_id": 10,
      "evaluatee_name": "김동료",
      "score": 85,
      "comment": "항상 적극적으로 도와주셔서 감사합니다."
    },
    {
      "evaluatee_id": 12,
      "evaluatee_name": "박동료",
      "score": null,
      "comment": null
    }
  ]
}
```

- **`status`**: 평가 진행 상태를 나타냅니다.
  - `"NOT_STARTED"`: 평가를 한 명도 진행하지 않음
  - `"IN_PROGRESS"`: 일부 동료에 대해서만 평가를 진행함
  - `"COMPLETED"`: 모든 동료에 대한 평가를 완료함

### 3.2. 실패

- **400 Bad Request**: 활성 평가 기간이 없는 경우
- **401 Unauthorized**: 인증 토큰이 유효하지 않은 경우
- **404 Not Found**: 해당 `project_id`를 가진 프로젝트가 존재하지 않는 경우
