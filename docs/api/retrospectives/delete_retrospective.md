# API: 회고록 삭제

- **HTTP Method:** `DELETE`
- **URL:** `/api/v1/retrospectives/{id}`
- **Description:** 현재 로그인한 사용자가 작성한 특정 회고록을 삭제합니다.
- **Permissions:** 로그인한 모든 사용자 (`employee` 이상). **자신의 회고록만** 삭제 가능합니다.

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

### Path Parameters
- **id** (int, required): 삭제할 회고록의 ID.

---

## Response

### Success
- **Status Code:** `204 No Content`
- **Body:** (없음)

### Errors
- **Status Code:** `401 Unauthorized`
- **Status Code:** `404 Not Found`
  - **Reason:** ID에 해당하는 회고록이 없거나, 다른 사용자의 회고록에 접근을 시도한 경우.
