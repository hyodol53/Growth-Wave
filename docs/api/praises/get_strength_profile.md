# API: 사용자 강점 프로필 조회

- **HTTP Method:** `GET`
- **URL:** `/api/v1/users/{user_id}/strength-profile`
- **Description:** 특정 사용자의 공개 강점 프로필을 조회합니다. 이 프로필에는 현재 활성 평가 기간 동안 집계된 강점 뱃지 목록이 포함됩니다.
- **Permissions:** 모든 사용자 (인증 불필요)

---

## Request

### Path Parameters
- **user_id** (int, required): 프로필을 조회할 사용자의 ID

---

## Response

### Success
- **Status Code:** `200 OK`
- **Body:**
  ```json
  {
    "user_id": 123,
    "full_name": "김성장",
    "current_period": "2025년 하반기",
    "badges": [
      {
        "hashtag": "#해결사",
        "count": 8
      },
      {
        "hashtag": "#소통왕",
        "count": 5
      },
      {
        "hashtag": "#협업왕",
        "count": 2
      }
    ]
  }
  ```
  - `badges` 목록은 칭찬을 많이 받은 순 (`count` 내림차순)으로 정렬됩니다.

### Errors
- **Status Code:** `404 Not Found`
  - **Reason:** `user_id`에 해당하는 사용자가 존재하지 않는 경우
    ```json
    { "detail": "User not found" }
    ```
- **Status Code:** `400 Bad Request`
  - **Reason:** 현재 시스템에 활성화된 평가 기간이 없는 경우
    ```json
    { "detail": "There is no active evaluation period." }
    ```
