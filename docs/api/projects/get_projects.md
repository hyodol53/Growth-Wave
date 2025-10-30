# API: 프로젝트 목록 조회 (GET /projects)

## 1. 개요

조건에 맞는 프로젝트 목록을 조회합니다. **특정 평가 기간(Evaluation Period)을 기준으로 조회하는 것을 권장합니다.**

## 2. 요청 (Request)

### 2.1. 엔드포인트 (Endpoint)

```
GET /api/v1/projects
```

### 2.2. 헤더 (Headers)

- `Authorization`: `Bearer <access_token>`

### 2.3. 쿼리 파라미터 (Query Parameters)

| 파라미터 | 타입 | 필수 여부 | 설명 |
| :--- | :--- | :--- | :--- |
| `evaluation_period_id` | integer | N | **(추가됨)** 특정 평가 기간 ID로 프로젝트를 필터링합니다. 미지정 시 모든 프로젝트가 조회될 수 있습니다. |
| `pm_id` | integer | N | 특정 PM이 담당하는 프로젝트를 필터링합니다. |
| `user_id` | integer | N | 특정 사용자가 참여하고 있는 프로젝트를 필터링합니다. |
| `skip` | integer | N | 페이지네이션을 위한 건너뛸 항목 수 (기본값: 0) |
| `limit` | integer | N | 페이지네이션을 위한 한 페이지의 항목 수 (기본값: 100) |

**사용 예시:**
- 3번 평가 기간에 속한 모든 프로젝트 조회: `GET /api/v1/projects?evaluation_period_id=3`
- 15번 사용자가 참여하는 프로젝트 조회: `GET /api/v1/projects?user_id=15`

## 3. 응답 (Response)

### 3.1. 성공 (Success)

- **Status Code:** `200 OK`
- **Body:**

```json
[
  {
    "id": 101,
    "name": "신규 성장 동력 발굴 TF",
    "pm_id": 15,
    "evaluation_period_id": 3,
    "start_date": "2024-07-01",
    "end_date": "2024-12-31",
    "created_at": "2024-05-20T10:00:00Z",
    "updated_at": "2024-05-20T10:00:00Z"
  },
  {
    "id": 102,
    "name": "기존 시스템 유지보수",
    "pm_id": 22,
    "evaluation_period_id": 3,
    "start_date": "2024-07-01",
    "end_date": "2024-12-31",
    "created_at": "2024-05-21T11:00:00Z",
    "updated_at": "2024-05-21T11:00:00Z"
  }
]
```

### 3.2. 실패 (Failure)

- **Status Code:** `401 Unauthorized` (인증 실패)
- **Status Code:** `422 Unprocessable Entity` (유효성 검사 오류)