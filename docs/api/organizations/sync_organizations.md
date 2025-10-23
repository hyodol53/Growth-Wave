# API: Sync Organizations from File

## `POST /api/v1/organizations/upload`

### 설명
JSON 또는 CSV 형식의 파일을 업로드하여 전체 조직도를 일괄적으로 동기화합니다. 파일의 내용을 기준으로 조직을 생성, 수정 또는 삭제합니다. (요구사항 ID: `FR-A-1.1`)

### 권한
- 관리자(Admin) 권한이 필요합니다.

### 요청 (Request)
- **Content-Type:** `multipart/form-data`
- **Body:**
    - `file`: 조직도 정보를 담고 있는 `JSON` 또는 `CSV` 파일

#### 파일 형식 예시 (JSON)
```json
[
  {
    "name": "AI 연구소",
    "level": 1,
    "parent": null,
    "children": [
      {
        "name": "플랫폼실",
        "level": 2,
        "children": [
          { "name": "코어팀", "level": 3 },
          { "name": "API팀", "level": 3 }
        ]
      }
    ]
  }
]
```

### 응답 (Response)
- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
      "message": "Organizations synced successfully",
      "created": 15,
      "updated": 5,
      "deleted": 2
    }
    ```
    - `created`: 새로 생성된 조직 수
    - `updated`: 정보가 변경된 조직 수
    - `deleted`: 삭제된 조직 수

### 발생 가능한 오류
- **`400 Bad Request`**: 파일이 없거나 지원하지 않는 파일 형식인 경우
- **`401 Unauthorized`**: 인증되지 않은 사용자의 요청인 경우
- **`403 Forbidden`**: 해당 작업을 수행할 권한이 없는 경우
