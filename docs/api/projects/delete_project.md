# 프로젝트 삭제

- **HTTP Method:** `DELETE`
- **URL:** `/api/v1/projects/{project_id}`
- **Description:** 지정된 ID를 가진 프로젝트를 삭제합니다.
- **Permissions:** `dept_head`, `admin`

---

### Request

- **Headers:**
    - `Authorization: Bearer <access_token>`
- **Path Parameters:**
    - `project_id` (integer, required): 삭제할 프로젝트의 ID

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
    *(삭제된 프로젝트의 정보가 반환됩니다.)*

---

### Error Responses

- **Status Code:** `403 Forbidden`
    - **Reason:** 요청자가 권한이 없거나, 다른 부서의 프로젝트를 삭제하려고 하는 경우
- **Status Code:** `404 Not Found`
    - **Reason:** `project_id`에 해당하는 프로젝트가 존재하지 않는 경우
