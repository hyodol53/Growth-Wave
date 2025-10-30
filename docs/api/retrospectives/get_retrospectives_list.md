# API: 내 회고록 목록 조회

- **HTTP Method:** `GET`
- **URL:** `/api/v1/retrospectives`
- **Description:** 현재 로그인한 사용자가 작성한 모든 회고록의 목록을 조회합니다.
- **Permissions:** 로그인한 모든 사용자 (`employee` 이상)

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

---

## Response

### Success
- **Status Code:** `200 OK`
- **Body:** 회고록 객체의 배열
  ```json
  [
    {
      "id": 2,
      "user_id": 123,
      "title": "2025년 하반기 회고록",
      "content": "...",
      "evaluation_period_id": 2,
      "created_at": "2025-12-31T18:00:00Z",
      "updated_at": null
    },
    {
      "id": 1,
      "user_id": 123,
      "title": "2025년 상반기 회고록",
      "content": "...",
      "evaluation_period_id": 1,
      "created_at": "2025-06-30T17:00:00Z",
      "updated_at": "2025-07-01T10:00:00Z"
    }
  ]
  ```

### Errors
- **Status Code:** `401 Unauthorized`
