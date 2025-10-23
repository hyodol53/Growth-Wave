# API: Get External Accounts

## `GET /api/v1/external-accounts/`

### 설명
현재 인증된 사용자가 시스템에 연동한 모든 외부 계정 목록을 조회합니다.

### 권한
- 인증된 사용자만 접근 가능합니다.

### 요청 (Request)
- 별도의 요청 본문이 필요하지 않습니다.

### 응답 (Response)
- **Status Code:** `200 OK`
- **Body:**
    ```json
    [
      {
        "id": 1,
        "account_type": "JIRA",
        "username": "user@example.com",
        "user_id": 123
      },
      {
        "id": 2,
        "account_type": "GITHUB",
        "username": "github_user",
        "user_id": 123
      }
    ]
    ```

### 발생 가능한 오류
- **`401 Unauthorized`**: 인증되지 않은 사용자의 요청인 경우
