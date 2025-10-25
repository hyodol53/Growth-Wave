# 사용자 정보 수정

- **HTTP Method:** `PUT`
- **URL:** `/api/v1/users/{user_id}`
- **Description:** 지정된 ID를 가진 사용자의 정보를 수정합니다. (소속 조직 변경, 역할 변경 등)
- **Permissions:** `admin`

---

### Request

- **Headers:**
    - `Authorization: Bearer <access_token>`
- **Path Parameters:**
    - `user_id` (integer, required): 수정할 사용자의 ID

- **Body:**
    ```json
    {
        "full_name": "Hyojae Jang",
        "email": "new.email@example.com",
        "organization_id": 5,
        "role": "team_lead"
    }
    ```
    *모든 필드는 선택적(Optional)입니다.*

---

### Response

- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
        "id": 2,
        "username": "testuser",
        "email": "new.email@example.com",
        "full_name": "Hyojae Jang",
        "role": "team_lead",
        "organization_id": 5
    }
    ```

---

### Error Responses

- **Status Code:** `403 Forbidden`
    - **Reason:** 요청자가 `admin` 권한을 가지고 있지 않은 경우
- **Status Code:** `404 Not Found`
    - **Reason:** `user_id`에 해당하는 사용자가 존재하지 않는 경우
- **Status Code:** `422 Unprocessable Entity`
    - **Reason:** 요청 본문의 데이터 형식이 잘못된 경우
