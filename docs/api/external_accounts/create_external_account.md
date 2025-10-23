# API: Create External Account

## `POST /api/v1/external-accounts/`

### 설명
사용자 본인의 외부 서비스 계정(Jira, GitHub, Bitbucket 등)을 시스템에 연동(등록)합니다. (요구사항 ID: `FR-B-1.1`)

### 권한
- 인증된 사용자만 접근 가능합니다.

### 요청 (Request)
- **Body (JSON):**
    ```json
    {
      "account_type": "JIRA",
      "username": "user@example.com",
      "access_token": "your_personal_access_token"
    }
    ```
    - `account_type` (str, required): 외부 서비스의 종류. (Enum: `JIRA`, `GITHUB`, `BITBUCKET`)
    - `username` (str, required): 외부 서비스에서의 사용자 이름 또는 아이디
    - `access_token` (str, required): 외부 서비스에서 발급받은 Personal Access Token (PAT) 또는 API 키

### 응답 (Response)
- **Status Code:** `201 OK`
- **Body:**
    ```json
    {
      "id": 1,
      "account_type": "JIRA",
      "username": "user@example.com",
      "user_id": 123
    }
    ```
    - **참고:** 보안을 위해 요청 시 보냈던 `access_token`은 응답에 포함되지 않습니다.

### 발생 가능한 오류
- **`400 Bad Request`**: 필수 필드가 누락되거나 `account_type`이 유효하지 않은 경우
- **`401 Unauthorized`**: 인증되지 않은 사용자의 요청인 경우
