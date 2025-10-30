# API: 외부 계정 연동 해제

- **HTTP Method:** `DELETE`
- **URL:** `/api/v1/external-accounts/{id}`
- **Description:** 현재 로그인한 사용자의 특정 외부 계정 연동을 해제(삭제)합니다.
- **Permissions:** 로그인한 모든 사용자 (`employee` 이상). 단, **자기 자신이 연동한 계정만** 삭제할 수 있습니다.

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

### Path Parameters
- **id** (int, required): 삭제할 외부 계정 연동 정보의 고유 ID.

---

## Response

### Success
- **Status Code:** `204 No Content`
- **Body:** (없음)

### Errors
- **Status Code:** `401 Unauthorized`
  - **Reason:** 인증 토큰이 없거나 유효하지 않은 경우.
- **Status Code:** `403 Forbidden`
  - **Reason:** 다른 사용자의 계정 정보를 삭제하려고 시도한 경우.
- **Status Code:** `404 Not Found`
  - **Reason:** `id`에 해당하는 계정 정보가 존재하지 않는 경우.