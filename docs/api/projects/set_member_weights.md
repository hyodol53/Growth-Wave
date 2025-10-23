# API: Set Project Member Weights

## `POST /api/v1/projects/members/weights`

### 설명
실장이 소속된 실의 인원들이 각 프로젝트에 참여하는 비중(%)을 설정합니다. 각 인원의 프로젝트 비중 총합은 100%가 되어야 합니다. (요구사항 ID: `FR-A-1.3`)

### 권한
- 실장(`DeptHead`) 역할의 사용자만 접근 가능합니다.

### 요청 (Request)
- **Body (JSON):**
    ```json
    [
      {
        "user_id": 101,
        "weights": [
          { "project_id": 1, "weight": 70 },
          { "project_id": 2, "weight": 30 }
        ]
      },
      {
        "user_id": 102,
        "weights": [
          { "project_id": 1, "weight": 100 }
        ]
      }
    ]
    ```
    - `user_id` (int): 비중을 설정할 직원의 ID
    - `weights` (array): 해당 직원이 참여하는 프로젝트와 비중의 목록
        - `project_id` (int): 프로젝트 ID
        - `weight` (int): 참여 비중 (%)

### 응답 (Response)
- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
      "message": "Project member weights updated successfully"
    }
    ```

### 발생 가능한 오류
- **`400 Bad Request`**:
    - 특정 유저의 비중 총합이 100이 아닌 경우
    - 요청 데이터의 형식이 잘못된 경우
- **`401 Unauthorized`**: 인증되지 않은 사용자의 요청인 경우
- **`403 Forbidden`**: 실장 권한이 없는 사용자가 요청한 경우
- **`404 Not Found`**: 요청에 포함된 `user_id` 또는 `project_id`가 존재하지 않는 경우
