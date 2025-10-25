# 프로젝트 생성

- **HTTP Method:** `POST`
- **URL:** `/api/v1/projects/`
- **Description:** 새로운 프로젝트를 생성합니다.
- **Permissions:** `dept_head`, `admin`

---

### Request

- **Headers:**
    - `Authorization: Bearer <access_token>`

- **Body:**
    ```json
    {
        "name": "Growth-Wave Development",
        "description": "A project to develop the dual-track HR platform.",
        "owner_org_id": 1
    }
    ```
    *실장(`dept_head`)은 `owner_org_id`를 자신이 속한 조직의 ID로만 지정할 수 있습니다.*

---

### Response

- **Status Code:** `201 Created`
- **Body:**
    ```json
    {
        "id": 1,
        "name": "Growth-Wave Development",
        "description": "A project to develop the dual-track HR platform.",
        "owner_org_id": 1
    }
    ```

---

### Error Responses

- **Status Code:** `403 Forbidden`
    - **Reason:** 요청자가 `dept_head` 또는 `admin` 권한을 가지고 있지 않거나, 실장이 다른 부서의 프로젝트를 생성하려고 하는 경우
- **Status Code:** `422 Unprocessable Entity`
    - **Reason:** 요청 본문의 데이터 형식이 잘못된 경우
