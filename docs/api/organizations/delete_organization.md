# 조직 삭제

- **HTTP Method:** `DELETE`
- **URL:** `/api/v1/organizations/{org_id}`
- **Description:** 지정된 ID를 가진 조직을 삭제합니다.
- **Permissions:** `admin`

---

### Request

- **Headers:**
    - `Authorization: Bearer <access_token>`
- **Path Parameters:**
    - `org_id` (integer, required): 삭제할 조직의 ID

---

### Response

- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
        "id": 1,
        "name": "Engineering Team",
        "level": 3,
        "department_grade": null,
        "parent_id": 10,
        "children": []
    }
    ```
    *(삭제된 조직의 정보가 반환됩니다.)*

---

### Error Responses

- **Status Code:** `403 Forbidden`
    - **Reason:** 요청자가 `admin` 권한을 가지고 있지 않은 경우
- **Status Code:** `404 Not Found`
    - **Reason:** `org_id`에 해당하는 조직이 존재하지 않는 경우
