# API: 특정 회고록 조회

- **HTTP Method:** `GET`
- **URL:** `/api/v1/retrospectives/{id}`
- **Description:** 현재 로그인한 사용자가 작성한 특정 회고록 한 건을 상세 조회합니다.
- **Permissions:** 로그인한 모든 사용자 (`employee` 이상). **자신의 회고록만** 조회 가능합니다.

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

### Path Parameters
- **id** (int, required): 조회할 회고록의 ID.

---

## Response

### Success
- **Status Code:** `200 OK`
- **Body:** 회고록 객체 전체
  ```json
  {
    "id": 1,
    "user_id": 123,
    "title": "2025년 상반기 회고록",
    "content": "## 주요 성과\n\nAPI 성능 개선 프로젝트를 성공적으로 마무리했습니다...",
    "evaluation_period_id": 1,
    "created_at": "2025-06-30T17:00:00Z",
    "updated_at": "2025-07-01T10:00:00Z"
  }
  ```

### Errors
- **Status Code:** `401 Unauthorized`
- **Status Code:** `404 Not Found`
  - **Reason:** ID에 해당하는 회고록이 없거나, 다른 사용자의 회고록에 접근을 시도한 경우.
