# API: 회고록 수정

- **HTTP Method:** `PUT`
- **URL:** `/api/v1/retrospectives/{id}`
- **Description:** 현재 로그인한 사용자가 작성한 특정 회고록의 제목이나 내용을 수정합니다.
- **Permissions:** 로그인한 모든 사용자 (`employee` 이상). **자신의 회고록만** 수정 가능합니다.

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

### Path Parameters
- **id** (int, required): 수정할 회고록의 ID.

### Body
```json
{
  "title": "2025년 상반기 회고록 (수정본)",
  "content": "새롭게 추가된 내용입니다..."
}
```
- **title** (str, optional): 수정할 회고록 제목.
- **content** (str, optional): 수정할 회고록 본문.

---

## Response

### Success
- **Status Code:** `200 OK`
- **Body:** 수정이 완료된 회고록 객체 전체
  ```json
  {
    "id": 1,
    "user_id": 123,
    "title": "2025년 상반기 회고록 (수정본)",
    "content": "새롭게 추가된 내용입니다...",
    "evaluation_period_id": 1,
    "created_at": "2025-06-30T17:00:00Z",
    "updated_at": "2025-10-31T14:00:00Z"
  }
  ```

### Errors
- **Status Code:** `401 Unauthorized`
- **Status Code:** `404 Not Found`
  - **Reason:** ID에 해당하는 회고록이 없거나, 다른 사용자의 회고록에 접근을 시도한 경우.
- **Status Code:** `422 Unprocessable Entity`
