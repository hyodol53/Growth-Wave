# API: Create User

## `POST /api/v1/users/`

### 설명
새로운 사용자를 시스템에 등록합니다.

### 요청 (Request)
- **Body (JSON):**
    ```json
    {
      "email": "user@example.com",
      "password": "string",
      "full_name": "string",
      "organization_id": 0
    }
    ```
    - `email` (str, required): 사용자 이메일 (로그인 ID로 사용)
    - `password` (str, required): 사용자 비밀번호
    - `full_name` (str, optional): 사용자 전체 이름
    - `organization_id` (int, optional): 사용자가 소속될 조직(부서)의 ID

### 응답 (Response)
- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
      "id": 0,
      "email": "user@example.com",
      "full_name": "string",
      "organization_id": 0,
      "is_active": true
    }
    ```

### 발생 가능한 오류
- **`400 Bad Request`**: 필수 필드가 누락되거나 형식이 잘못된 경우
- **`409 Conflict`**: 이미 동일한 이메일을 가진 사용자가 존재하는 경우
