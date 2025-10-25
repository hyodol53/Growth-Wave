# 사용자 삭제

- **HTTP Method:** `DELETE`
- **URL:** `/api/v1/users/{user_id}`
- **Description:** 지정된 ID를 가진 사용자를 삭제합니다.
- **Permissions:** `admin`

---

### Request

- **Headers:**
    - `Authorization: Bearer <access_token>`
- **Path Parameters:**
    - `user_id` (integer, required): 삭제할 사용자의 ID

---

### Response

- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
        "id": 2,
        "username": "testuser",
        "email": "test.user@example.com",
        "full_name": "Test User",
        "role": "employee",
        "organization_id": 1
    }
    ```
    *(삭제된 사용자의 정보가 반환됩니다.)*

---

### Error Responses

- **Status Code:** `403 Forbidden`
    - **Reason:** 요청자가 `admin` 권한을 가지고 있지 않은 경우
- **Status Code:** `404 Not Found`
    - **Reason:** `user_id`에 해당하는 사용자가 존재하지 않는 경우
