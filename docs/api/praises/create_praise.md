# API: 칭찬 전송

- **HTTP Method:** `POST`
- **URL:** `/api/v1/praises`
- **Description:** 다른 사용자에게 익명으로 칭찬 메시지와 강점 해시태그를 전송합니다.
- **Permissions:** 로그인한 모든 사용자 (`employee` 이상)

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

### Body
```json
{
  "recipient_id": 123,
  "message": "오늘 발표 정말 인상적이었습니다! 명확하게 설명해주셔서 이해가 잘 됐어요.",
  "hashtag": "#소통왕"
}
```
- **recipient_id** (int, required): 칭찬을 받을 사용자의 ID
- **message** (str, required): 칭찬 메시지 본문 (1~500자)
- **hashtag** (str, required): 시스템에 정의된 강점 해시태그 중 하나. (예: `"#해결사"`, `"#소통왕"`)

---

## Response

### Success
- **Status Code:** `201 Created`
- **Body:**
  ```json
  {
    "message": "Praise sent successfully"
  }
  ```

### Errors
- **Status Code:** `400 Bad Request`
  - **Reason:** 자기 자신에게 칭찬을 보낸 경우
    ```json
    { "detail": "You cannot praise yourself." }
    ```
  - **Reason:** 활성 평가 기간이 없는 경우
    ```json
    { "detail": "There is no active evaluation period." }
    ```
  - **Reason:** 유효하지 않은 해시태그를 사용한 경우
    ```json
    { "detail": "Invalid hashtag. Available hashtags are: [...]" }
    ```
  - **Reason:** 평가 기간 내 동일인에 대한 칭찬 횟수 제한을 초과한 경우
    ```json
    { "detail": "You have already praised this person 5 times in this period." }
    ```
- **Status Code:** `401 Unauthorized`
  - **Reason:** 인증 토큰이 없거나 유효하지 않은 경우
- **Status Code:** `422 Unprocessable Entity`
  - **Reason:** 요청 본문의 형식이 유효하지 않은 경우 (예: `recipient_id`가 숫자가 아님)
