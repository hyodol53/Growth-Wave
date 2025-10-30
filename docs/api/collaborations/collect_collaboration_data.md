# API: 협업 데이터 수집 실행

- **HTTP Method:** `POST`
- **URL:** `/api/v1/collaborations/collect`
- **Description:** 시스템에 등록된 모든 사용자의 연동된 외부 계정(Jira, Bitbucket 등)으로부터 협업 데이터를 수집하는 프로세스를 실행합니다. 이 작업은 시간이 걸릴 수 있습니다.
- **Permissions:** **관리자 (`admin`)만** 실행 가능합니다.

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

---

## Response

### Success
- **Status Code:** `202 Accepted`
- **Body:**
  ```json
  {
    "message": "Collection process started.",
    "total_new_interactions": 0 
  }
  ```
  - **total_new_interactions**: 이번 수집을 통해 새로 추가된 협업 데이터의 수. (현재 구현은 동기식이므로 즉시 결과를 반환하지만, 향후 비동기 처리로 변경될 수 있습니다.)

### Errors
- **Status Code:** `401 Unauthorized`
  - **Reason:** 인증 토큰이 없거나 유효하지 않은 경우.
- **Status Code:** `403 Forbidden`
  - **Reason:** 관리자 권한이 없는 사용자가 API를 호출한 경우.