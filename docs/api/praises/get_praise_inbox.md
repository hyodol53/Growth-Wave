# API: 내 칭찬 인박스 조회

- **HTTP Method:** `GET`
- **URL:** `/api/v1/praises/inbox`
- **Description:** 현재 로그인한 사용자가 받은 모든 칭찬 메시지를 조회합니다. 발신자는 '익명의 형용사+동물' 형태로 표시됩니다.
- **Permissions:** 로그인한 모든 사용자 (`employee` 이상)

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

---

## Response

### Success
- **Status Code:** `200 OK`
- **Body:**
  ```json
  [
    {
      "sender_display_name": "익명의 용감한 고라니",
      "message": "오늘 발표 정말 인상적이었습니다!",
      "hashtag": "#소통왕",
      "received_at": "2025-10-31T10:30:00Z"
    },
    {
      "sender_display_name": "익명의 현명한 수달",
      "message": "지난번 문제 해결에 큰 도움 주셔서 감사합니다.",
      "hashtag": "#해결사",
      "received_at": "2025-10-28T15:00:00Z"
    }
  ]
  ```
  - 응답은 칭찬을 받은 최신순 (`received_at` 내림차순)으로 정렬됩니다.

### Errors
- **Status Code:** `401 Unauthorized`
  - **Reason:** 인증 토큰이 없거나 유효하지 않은 경우
