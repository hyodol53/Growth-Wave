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
        "description": "Focus on Track-A features.",
        "pm_id": 124
    }
    ```
    *모든 필드는 선택적(Optional)입니다. 실장은 자신이 속한 부서의 멤버가 PM인 프로젝트만 수정할 수 있으며, PM을 변경할 경우에도 같은 부서 내의 멤버로만 지정할 수 있습니다.*

---

### Response

- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
        "id": 1,
        "name": "Growth-Wave Phase 2",
        "description": "Focus on Track-A features.",
        "pm_id": 124,
        "start_date": null,
        "end_date": null,
        "pm": {
            "id": 124,
            "username": "new_pm",
            "email": "new_pm@example.com",
            "full_name": "New PM",
            "title": "Senior Engineer",
            "role": "employee",
            "organization_id": 1
        }
    }
    ```

---

### Error Responses

- **Status Code:** `403 Forbidden`
    - **Reason:** 요청자가 권한이 없거나, 다른 부서의 프로젝트를 수정하려고 하는 경우
- **Status Code:** `404 Not Found`
    - **Reason:** `project_id`에 해당하는 프로젝트가 존재하지 않거나, `pm_id`로 지정된 사용자가 존재하지 않는 경우
- **Status Code:** `422 Unprocessable Entity`
    - **Reason:** 요청 본문의 데이터 형식이 잘못된 경우