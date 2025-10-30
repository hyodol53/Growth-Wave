# API: 프로젝트 생성 (POST /projects)

## 1. 개요

실장 이상의 보직자가 새로운 프로젝트를 생성합니다.

**중요:** 프로젝트는 반드시 특정 평가 기간(Evaluation Period)에 귀속되어야 합니다.

## 2. 요청 (Request)

### 2.1. 엔드포인트 (Endpoint)

```
POST /api/v1/projects
```

### 2.2. 헤더 (Headers)

- `Authorization`: `Bearer <access_token>`

### 2.3. 본문 (Body)

```json
{
  "name": "신규 성장 동력 발굴 TF",
  "pm_id": 15,
  "evaluation_period_id": 3,
  "start_date": "2024-07-01",
  "end_date": "2024-12-31"
}
```

| 필드명 | 타입 | 필수 여부 | 설명 |
| :--- | :--- | :--- | :--- |
| `name` | string | Y | 프로젝트명 |
| `pm_id` | integer | Y | 프로젝트를 담당하는 PM의 사용자 ID |
| `evaluation_period_id` | integer | Y | **(수정됨)** 프로젝트가 귀속될 평가 기간의 ID |
| `start_date` | string | N | 프로젝트 시작일 (YYYY-MM-DD). 프로젝트 자체의 생명주기를 나타냅니다. |
| `end_date` | string | N | 프로젝트 종료일 (YYYY-MM-DD). 프로젝트 자체의 생명주기를 나타냅니다. |

## 3. 응답 (Response)

### 3.1. 성공 (Success)

- **Status Code:** `201 Created`
- **Body:**

```json
{
  "id": 101,
  "name": "신규 성장 동력 발굴 TF",
  "pm_id": 15,
  "evaluation_period_id": 3,
  "start_date": "2024-07-01",
  "end_date": "2024-12-31",
  "created_at": "2024-05-20T10:00:00Z",
  "updated_at": "2024-05-20T10:00:00Z"
}
```

### 3.2. 실패 (Failure)

- **Status Code:** `400 Bad Request` (필수 필드 누락 등)
- **Status Code:** `401 Unauthorized` (인증 실패)
- **Status Code:** `403 Forbidden` (권한 없음)
- **Status Code:** `404 Not Found` (pm_id 또는 evaluation_period_id가 존재하지 않음)
- **Status Code:** `422 Unprocessable Entity` (유효성 검사 오류)
