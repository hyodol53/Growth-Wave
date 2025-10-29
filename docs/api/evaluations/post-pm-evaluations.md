# `POST /api/v1/evaluations/pm-evaluations/`

## 1. 개요

현재 로그인한 사용자(PM)가 특정 프로젝트의 구성원들에 대한 PM 평가를 **생성하거나 수정(UPSERT)**합니다.

## 2. 변경사항 (v2)

- **`comment` 필드 추가**: 서술형 피드백을 남길 수 있는 `comment` 필드가 추가되었습니다.
- **UPSERT 기능**: 동일한 `(project_id, evaluator_id, evaluatee_id, evaluation_period)`에 대한 평가 데이터가 이미 존재할 경우, 새로운 데이터를 생성하는 대신 기존 데이터의 `score`와 `comment`를 덮어씁니다.

## 3. 요청

### 3.1. Headers

| Key | Value | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `Authorization` | `Bearer <JWT_TOKEN>` | O | 사용자의 JWT Access Token |

### 3.2. Body

**Content-Type:** `application/json`

```json
{
  "evaluations": [
    {
      "project_id": 1,
      "evaluatee_id": 2,
      "score": 85,
      "comment": "피드백 내용입니다."
    },
    {
      "project_id": 1,
      "evaluatee_id": 3,
      "score": 90,
      "comment": "수정된 피드백입니다."
    }
  ]
}
```

## 4. 응답

### 4.1. 성공 (200 OK)

**Content-Type:** `application/json`

- 생성 또는 수정된 평가 데이터 객체의 리스트를 반환합니다.

### 4.2. 실패

- **400 Bad Request**:
  - 활성 평가 기간이 없는 경우
  - 점수가 0-100 범위를 벗어나는 경우
- **401 Unauthorized**: 인증 토큰이 유효하지 않은 경우
- **403 Forbidden**: 요청을 보낸 사용자가 해당 프로젝트의 PM이 아닌 경우
