# GET /api/v1/evaluations/me

## API 설명
현재 로그인한 사용자가 자신의 최종 평가 결과를 조회합니다.

이 API는 요구사항 `FR-A-5.1`을 충족하며, 피평가자는 자신의 최종 등급과 각 PM에게 받은 PM 평가 점수만 열람할 수 있습니다.

## 요청 (Request)

### URL
`GET /api/v1/evaluations/me`

### 헤더 (Headers)
- `Authorization`: `Bearer <ACCESS_TOKEN>`

### 쿼리 파라미터 (Query Parameters)
- `evaluation_period` (string, optional): 조회할 평가 기간 (예: "2025-H1"). 지정하지 않으면 현재 날짜를 기준으로 자동으로 설정됩니다.

## 응답 (Response)

### 성공 (Success)
- **상태 코드:** `200 OK`
- **본문 (Body):** `MyEvaluationResult` 스키마
```json
{
  "evaluation_period": "2025-H1",
  "grade": "A",
  "pm_scores": [
    {
      "project_name": "Growth-Wave 개발",
      "pm_name": "홍길동",
      "score": 90
    }
  ]
}
```

### 실패 (Failure)
- **상태 코드:** `401 Unauthorized`
  - **원인:** 인증되지 않은 사용자의 요청
  - **본문:**
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- **상태 코드:** `404 Not Found`
  - **원인:** 해당 평가 기간에 대한 최종 평가 데이터가 존재하지 않을 경우 (참고: 이 경우 API는 성공적으로 200을 반환하되 `grade` 필드가 `null`일 수 있습니다.)
