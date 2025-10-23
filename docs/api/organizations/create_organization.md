# API: Create Organization

## `POST /api/v1/organizations/`

### 설명
새로운 조직(부서)을 생성합니다.

### 권한
- 인증된 사용자만 접근 가능합니다.

### 요청 (Request)
- **Body (JSON):**
    ```json
    {
      "name": "string",
      "level": 0,
      "parent_id": 0
    }
    ```
    - `name` (str, required): 조직 이름
    - `level` (int, required): 조직의 레벨 (1: 센터, 2: 실, 3: 팀)
    - `parent_id` (int, optional): 상위 조직의 ID. 최상위 조직인 경우 `null` 또는 생략.

### 응답 (Response)
- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
      "id": 0,
      "name": "string",
      "level": 0,
      "parent_id": 0
    }
    ```

### 발생 가능한 오류
- **`400 Bad Request`**: 필수 필드가 누락되거나 형식이 잘못된 경우
- **`401 Unauthorized`**: 인증되지 않은 사용자의 요청인 경우
