# API: 연동된 외부 계정 목록 조회

- **HTTP Method:** `GET`
- **URL:** `/api/v1/external-accounts`
- **Description:** 현재 로그인한 사용자가 연동한 모든 외부 계정의 목록을 조회합니다.
- **Permissions:** 로그인한 모든 사용자 (`employee` 이상)

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

---

## Response

### Success
- **Status Code:** `200 OK`
- **Body:**
  ```json
  [
    {
      "id": 1,
      "provider": "jira",
      "account_id": "user@example.com"
    },
    {
      "id": 2,
      "provider": "bitbucket",
      "account_id": "my_bitbucket_user"
    }
  ]
  ```

### Errors
- **Status Code:** `401 Unauthorized`
  - **Reason:** 인증 토큰이 없거나 유효하지 않은 경우.