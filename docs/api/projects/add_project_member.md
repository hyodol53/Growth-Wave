# 프로젝트 멤버 추가

- **HTTP Method:** `POST`
- **URL:** `/api/v1/projects/{project_id}/members`
- **Description:** 특정 프로젝트에 새로운 멤버를 배정합니다. 멤버의 참여 비중(participation_weight)은 해당 멤버의 현재 비중 총합을 기반으로 자동으로 계산됩니다.
- **Permissions:** `dept_head`, `admin`

---

### Request

- **Headers:**
    - `Authorization: Bearer <access_token>`
- **Path Parameters:**
    - `project_id` (integer, required): 멤버를 추가할 프로젝트의 ID

- **Body:**
    ```json
    {
        "user_id": 25,
        "is_pm": false
    }
    ```
    - `user_id` (integer, required): 프로젝트에 추가할 사용자의 ID
    - `is_pm` (boolean, optional): 해당 멤버가 PM인지 여부 (기본값: `false`)

    *실장(`dept_head`)은 자신이 관리하는 프로젝트(PM이 자신의 부서 소속인 프로젝트)에 자신의 부서 멤버만 추가할 수 있습니다.*
    *관리자(`admin`)는 이러한 제약 없이 모든 프로젝트에 모든 사용자를 추가할 수 있습니다.*

---

### Response

- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
        "user_id": 25,
        "project_id": 1,
        "is_pm": false,
        "participation_weight": 40,
        "id": 101
    }
    ```
    *사용자의 다른 프로젝트 참여 비중 총합이 60%였을 경우, 새로 추가된 이 프로젝트의 비중은 40으로 자동 계산됩니다.*

---

### Error Responses

- **Status Code:** `403 Forbidden`
    - **Reason:** 요청자가 권한이 없거나, 다른 부서의 프로젝트에 멤버를 추가하려고 하는 경우
- **Status Code:** `404 Not Found`
    - **Reason:** `project_id`에 해당하는 프로젝트가 없거나, `user_id`에 해당하는 사용자가 없는 경우
- **Status Code:** `409 Conflict`
    - **Reason:** 사용자가 이미 해당 프로젝트의 멤버인 경우
- **Status Code:** `422 Unprocessable Entity`
    - **Reason:** 요청 본문의 데이터 형식이 잘못된 경우
