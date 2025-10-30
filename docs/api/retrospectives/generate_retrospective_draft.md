# API: AI 회고록 초안 생성

- **HTTP Method:** `POST`
- **URL:** `/api/v1/retrospectives/generate`
- **Description:** 현재 로그인한 사용자의 외부 계정 활동 내역을 기반으로 AI(Gemini Pro)를 사용하여 회고록 초안을 생성합니다. **이 API는 생성된 텍스트를 반환할 뿐, 데이터베이스에 저장하지는 않습니다.**
- **Permissions:** 로그인한 모든 사용자 (`employee` 이상)

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

### Body
(없음)

---

## Response

### Success
- **Status Code:** `200 OK`
- **Body:**
  ```json
  {
    "content": "## 주요 성과\n\n* **API 성능 개선 (PROJ-123):** 캐싱 레이어를 도입하여 주요 API의 응답 속도를 50% 향상시켰습니다...\n\n## 문제 해결 경험\n\n* **로그인 시스템 버그 수정 (PROJ-145):** OAuth2 인증 과정에서 발생하던 리다이렉트 오류를 해결하여...\n\n(AI가 생성한 전체 회고록 텍스트)"
  }
  ```

### Errors
- **Status Code:** `400 Bad Request`
  - **Reason:** `GOOGLE_API_KEY`가 설정되지 않은 경우.
- **Status Code:** `401 Unauthorized`
  - **Reason:** 인증 토큰이 없거나 유효하지 않은 경우.
- **Status Code:** `503 Service Unavailable`
  - **Reason:** 외부 LLM 서비스(Gemini) 호출 중 오류가 발생한 경우.

