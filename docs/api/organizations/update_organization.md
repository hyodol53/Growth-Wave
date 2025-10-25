# 조직 정보 수정

- **HTTP Method:** `PUT`
- **URL:** `/api/v1/organizations/{org_id}`
- **Description:** 지정된 ID를 가진 조직의 정보를 수정합니다.
- **Permissions:** `admin`

---

### Request

- **Headers:**
    - `Authorization: Bearer <access_token>`
- **Path Parameters:**
    - `org_id` (integer, required): 수정할 조직의 ID

- **Body:**
    ```json
    {
        "name": "Updated Engineering Team",
        "level": 3,
        "parent_id": 10
    }
    ```
    *모든 필드는 선택적(Optional)입니다.*

---

### Response

- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
        "id": 1,
        "name": "Updated Engineering Team",
        "level": 3,
        "department_grade": null,
        "parent_id": 10,
        "children": []
    }
    ```

---

### Error Responses

- **Status Code:** `403 Forbidden`
    - **Reason:** 요청자가 `admin` 권한을 가지고 있지 않은 경우
- **Status Code:** `404 Not Found`
    - **Reason:** `org_id`에 해당하는 조직이 존재하지 않는 경우
- **Status Code:** `422 Unprocessable Entity`
    - **Reason:** 요청 본문의 데이터 형식이 잘못된 경우
