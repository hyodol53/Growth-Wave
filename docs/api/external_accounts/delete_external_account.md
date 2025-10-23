# API: Delete External Account

## `DELETE /api/v1/external-accounts/{account_id}`

### 설명
사용자 본인이 시스템에 연동한 외부 계정의 연결을 끊습니다(삭제합니다).

### 권한
- 인증된 사용자만 접근 가능하며, **본인의 계정만** 삭제할 수 있습니다.

### 요청 (Request)
- **Path Parameter:**
    - `account_id` (int, required): 삭제할 외부 계정의 `id`

### 응답 (Response)
- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
      "message": "External account deleted successfully"
    }
    ```

### 발생 가능한 오류
- **`401 Unauthorized`**: 인증되지 않은 사용자의 요청인 경우
- **`403 Forbidden`**: 다른 사용자의 계정을 삭제하려고 시도하는 경우
- **`404 Not Found`**: 해당 `account_id`를 가진 계정이 존재하지 않는 경우
