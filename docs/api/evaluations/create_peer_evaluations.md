# POST /api/v1/evaluations/peer-evaluations/

## API 설명

현재 로그인한 사용자가 프로젝트 동료들에게 동료 평가 점수를 제출하는 API입니다. 이 API는 여러 명의 동료에 대한 평가를 한 번에 제출할 수 있도록 지원하며, 제출된 점수의 평균이 특정 기준(70점)을 초과하지 않도록 유효성을 검사합니다.

## 권한

- 인증된 사용자 (모든 역할)

## 요청 (Request)

### HTTP 메서드 및 URL
`POST /api/v1/evaluations/peer-evaluations/`

### 헤더
`Authorization: Bearer <access_token>`

### 본문 (Body)
`application/json` 타입의 배열로, 각 객체는 다음 필드를 포함합니다.

```json
{
  "evaluations": [
    {
      "project_id": 1, 
      "evaluatee_id": 2, 
      "score": 65
    },
    {
      "project_id": 1, 
      "evaluatee_id": 3, 
      "score": 70
    }
  ]
}
```

**필드 설명:**
- `project_id` (integer, 필수): 평가가 이루어지는 프로젝트의 고유 ID.
- `evaluatee_id` (integer, 필수): 평가를 받는 동료 사용자의 고유 ID.
- `score` (integer, 필수): 동료에게 부여하는 점수 (0-100).

## 응답 (Response)

### 성공 응답 (200 OK)

평가가 성공적으로 제출되면, 생성된 동료 평가 객체들의 배열을 반환합니다.

```json
[
  {
    "project_id": 1,
    "evaluatee_id": 2,
    "score": 65,
    "id": 1,
    "evaluator_id": 1,
    "evaluation_period": "2025-H2"
  },
  {
    "project_id": 1,
    "evaluatee_id": 3,
    "score": 70,
    "id": 2,
    "evaluator_id": 1,
    "evaluation_period": "2025-H2"
  }
]
```

**필드 설명:**
- `id` (integer): 생성된 동료 평가의 고유 ID.
- `project_id` (integer): 평가가 이루어진 프로젝트의 고유 ID.
- `evaluator_id` (integer): 평가를 제출한 사용자의 고유 ID.
- `evaluatee_id` (integer): 평가를 받은 동료 사용자의 고유 ID.
- `score` (integer): 부여된 점수.
- `evaluation_period` (string): 평가가 속한 기간 (예: "2025-H1", "2025-H2").

### 오류 응답

- **400 Bad Request**
  - **원인:** 제출된 평가 점수의 평균이 70점을 초과하는 경우.
  ```json
  {
    "detail": "Average score cannot exceed 70."
  }
  ```
  - **원인:** 요청 본문의 형식이 유효하지 않거나 필수 필드가 누락된 경우.
  ```json
  {
    "detail": [
      {
        "loc": [
          "body",
          "evaluations",
          0,
          "project_id"
        ],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

- **401 Unauthorized**
  - **원인:** 유효한 인증 토큰이 제공되지 않은 경우.
  ```json
  {
    "detail": "Not authenticated"
  }
  ```

- **403 Forbidden**
  - **원인:** 현재 사용자가 해당 작업을 수행할 권한이 없는 경우 (예: 평가 기간이 아니거나, 평가 대상이 아닌 경우 등 - 현재 구현에는 없으나 향후 추가될 수 있는 유효성 검사).
  ```json
  {
    "detail": "Not enough privileges"
  }
  ```