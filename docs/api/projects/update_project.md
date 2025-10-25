# 프로젝트 수정

- **HTTP Method:** `PUT`
- **URL:** `/api/v1/projects/{project_id}`
- **Description:** 지정된 ID를 가진 프로젝트의 정보를 수정합니다.
- **Permissions:** `dept_head`, `admin`

---

### Request

- **Headers:**
    - `Authorization: Bearer <access_token>`
- **Path Parameters:**
    - `project_id` (integer, required): 수정할 프로젝트의 ID

- **Body:**
    ```json
    {
        "name": "Growth-Wave Phase 2",
        "description": "Focus on Track-A features."
    }
    ```
    *모든 필드는 선택적(Optional)입니다. 실장은 자신이 속한 부서의 프로젝트만 수정할 수 있습니다.*

---

### Response

- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
        "id": 1,
        "name": "Growth-Wave Phase 2",
        "description": "Focus on Track-A features.",
        "owner_org_id": 1
    }
    ```

---

### Error Responses

- **Status Code:** `403 Forbidden`
    - **Reason:** 요청자가 권한이 없거나, 다른 부서의 프로젝트를 수정하려고 하는 경우
- **Status Code:** `404 Not Found`
    - **Reason:** `project_id`에 해당하는 프로젝트가 존재하지 않는 경우
- **Status Code:** `422 Unprocessable Entity`
    - **Reason:** 요청 본문의 데이터 형식이 잘못된 경우
