# API: 외부 계정 연동

- **HTTP Method:** `POST`
- **URL:** `/api/v1/external-accounts`
- **Description:** 현재 로그인한 사용자의 새로운 외부 시스템 계정(Jira, Bitbucket 등)을 연동합니다. 인증 정보(API 토큰 등)는 암호화되어 안전하게 저장됩니다.
- **Permissions:** 로그인한 모든 사용자 (`employee` 이상)

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

### Body
```json
{
  "provider": "jira",
  "account_id": "user@example.com",
  "credentials": "your-jira-api-token-here"
}
```
- **provider** (str, required): 연동할 시스템의 종류. (`"jira"`, `"bitbucket"`)
- **account_id** (str, required): 외부 시스템에서 사용하는 계정 식별자 (예: 이메일 주소, 사용자 이름).
- **credentials** (str, required): API 토큰, OAuth 토큰 등 외부 시스템 접근에 필요한 인증 정보.

---

## Response

### Success
- **Status Code:** `201 Created`
- **Body:**
  ```json
  {
    "id": 1,
    "provider": "jira",
    "account_id": "user@example.com"
  }
  ```
  **참고:** 보안을 위해 요청 시 보냈던 `credentials` 정보는 절대 응답에 포함되지 않습니다.

### Errors
- **Status Code:** `401 Unauthorized`
  - **Reason:** 인증 토큰이 없거나 유효하지 않은 경우.
- **Status Code:** `422 Unprocessable Entity`
  - **Reason:** 요청 본문의 형식이 유효하지 않은 경우 (예: `provider`가 유효한 Enum 값이 아님).