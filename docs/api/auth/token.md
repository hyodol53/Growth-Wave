# API: Get Access Token

## `POST /api/v1/auth/token`

### 설명
사용자의 아이디(이메일)와 비밀번호를 사용하여 인증하고, 유효한 경우 API 접근에 필요한 JWT(JSON Web Token)를 발급합니다.

### 요청 (Request)
- **Content-Type:** `application/x-www-form-urlencoded`
- **Body:**
    - `username` (str, required): 사용자 이메일 주소
    - `password` (str, required): 사용자 비밀번호

### 응답 (Response)
- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
      "access_token": "string",
      "token_type": "bearer"
    }
    ```
    - `access_token`: API 요청 시 `Authorization` 헤더에 사용될 JWT
    - `token_type`: 토큰 유형 (항상 "bearer")

### 발생 가능한 오류
- **`401 Unauthorized`**: 아이디 또는 비밀번호가 잘못된 경우
