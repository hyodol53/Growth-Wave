# API: 회고록 저장

- **HTTP Method:** `POST`
- **URL:** `/api/v1/retrospectives`
- **Description:** 사용자가 작성하거나 AI 초안을 수정한 최종 회고록을 데이터베이스에 저장합니다.
- **Permissions:** 로그인한 모든 사용자 (`employee` 이상)

---

## Request

### Headers
- `Authorization: Bearer <access_token>`

### Body
```json
{
  "title": "2025년 상반기 회고록",
  "content": "## 주요 성과\n\nAPI 성능 개선 프로젝트를 성공적으로 마무리했습니다...",
  "evaluation_period_id": 1
}
```
- **title** (str, required): 회고록 제목.
- **content** (str, required): 회고록 본문.
- **evaluation_period_id** (int, optional): 회고록을 귀속시킬 평가 기간의 ID.

---

## Response

### Success
- **Status Code:** `201 Created`
- **Body:** 저장된 회고록 객체 전체
  ```json
  {
    "id": 1,
    "user_id": 123,
    "title": "2025년 상반기 회고록",
    "content": "## 주요 성과\n\nAPI 성능 개선 프로젝트를 성공적으로 마무리했습니다...",
    "evaluation_period_id": 1,
    "created_at": "2025-10-31T13:00:00Z",
    "updated_at": null
  }
  ```

### Errors
- **Status Code:** `401 Unauthorized`
- **Status Code:** `422 Unprocessable Entity`

```