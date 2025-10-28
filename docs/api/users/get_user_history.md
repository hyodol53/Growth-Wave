# 사용자 이력 조회

- **HTTP Method:** `GET`
- **URL:**
    - `/api/v1/users/me/history` (본인 이력 조회)
    - `/api/v1/users/{user_id}/history` (타인 이력 조회)
- **Description:** 지정된 사용자의 반기별 평가 결과 및 프로젝트 참여 이력을 조회합니다.
- **Permissions:**
    - `/me/history`: 모든 로그인한 사용자
    - `/{user_id}/history`: `dept_head`, `admin` (요청자는 대상 사용자의 상위 보직자이거나 관리자여야 함)

---

### Request

- **Headers:**
    - `Authorization: Bearer <access_token>`
- **Path Parameters (타인 이력 조회 시):**
    - `user_id` (integer, required): 조회할 사용자의 ID

---

### Response

- **Status Code:** `200 OK`
- **Body:**
    ```json
    {
        "history": [
            {
                "evaluation_period": "2024-H1",
                "final_evaluation": {
                    "evaluatee_id": 1,
                    "evaluation_period": "2024-H1",
                    "peer_score": 85.0,
                    "pm_score": 92.0,
                    "qualitative_score": 90.0,
                    "final_score": 89.5,
                    "grade": "A",
                    "id": 1
                },
                "projects": [
                    {
                        "project_id": 101,
                        "project_name": "Project Alpha",
                        "participation_weight": 70,
                        "is_pm": true
                    },
                    {
                        "project_id": 102,
                        "project_name": "Project Beta",
                        "participation_weight": 30,
                        "is_pm": false
                    }
                ]
            },
            {
                "evaluation_period": "2023-H2",
                "final_evaluation": null,
                "projects": []
            }
        ]
    }
    ```

---

### Error Responses

- **Status Code:** `401 Unauthorized`
    - **Reason:** 인증되지 않은 사용자의 요청
- **Status Code:** `403 Forbidden`
    - **Reason:** 권한 없는 사용자가 타인의 이력을 조회하려고 하는 경우
- **Status Code:** `404 Not Found`
    - **Reason:** `user_id`에 해당하는 사용자가 존재하지 않는 경우
