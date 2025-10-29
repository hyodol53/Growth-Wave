# `GET /api/v1/evaluations/pm-evaluations/{project_id}`

## 1. 개요

특정 프로젝트(`project_id`)에 대해, 현재 로그인한 사용자(PM)가 평가해야 할 프로젝트 구성원 목록과 이미 제출한 평가 내용(점수, 코멘트)을 조회합니다. 프론트엔드에서 PM이 평가를 진행할 때 기존에 저장된 내용을 채우는 데 사용됩니다.

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
  "members_to_evaluate": [
    {
      "evaluatee_id": 10,
      "evaluatee_name": "김멤버",
      "score": 90,
      "comment": "업무 이해도가 높고 성실합니다."
    },
    {
      "evaluatee_id": 12,
      "evaluatee_name": "박멤버",
      "score": null,
      "comment": null
    }
  ]
}
```

- **`status`**: 평가 진행 상태를 나타냅니다.
  - `"NOT_STARTED"`: 평가를 한 명도 진행하지 않음
  - `"IN_PROGRESS"`: 일부 멤버에 대해서만 평가를 진행함
  - `"COMPLETED"`: 모든 멤버에 대한 평가를 완료함

### 3.2. 실패

- **400 Bad Request**: 활성 평가 기간이 없는 경우
- **401 Unauthorized**: 인증 토큰이 유효하지 않은 경우
- **403 Forbidden**: 요청을 보낸 사용자가 해당 프로젝트의 PM이 아닌 경우
- **404 Not Found**: 해당 `project_id`를 가진 프로젝트가 존재하지 않는 경우
