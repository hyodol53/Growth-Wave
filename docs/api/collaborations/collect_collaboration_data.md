# API: 협업 데이터 수집

## `POST /api/v1/collaborations/collect`

### 1. 개요

외부 시스템(Jira, Bitbucket 등)의 백그라운드 데이터 수집기가 수집한 사용자 간의 상호작용 데이터를 시스템에 저장합니다.

### 2. 접근 권한

- **관리자 (`admin`)** 전용

### 3. 요청 (Request)

#### 3.1. 헤더 (Headers)

```json
{
  "Authorization": "Bearer <admin_access_token>"
}
```

#### 3.2. 본문 (Body)

```json
[
  {
    "source_user_id": 1,
    "target_user_id": 2,
    "project_id": 1,
    "interaction_type": "jira_comment",
    "occurred_at": "2025-10-24T10:00:00Z"
  },
  {
    "source_user_id": 2,
    "target_user_id": 1,
    "project_id": 1,
    "interaction_type": "bitbucket_pr_review",
    "occurred_at": "2025-10-24T11:30:00Z"
  }
]
```

### 4. 응답 (Response)

#### 4.1. 성공 (Success)

- **상태 코드:** `200 OK`
- **본문:**

```json
[
  {
    "source_user_id": 1,
    "target_user_id": 2,
    "project_id": 1,
    "interaction_type": "jira_comment",
    "occurred_at": "2025-10-24T10:00:00Z",
    "id": 1
  },
  {
    "source_user_id": 2,
    "target_user_id": 1,
    "project_id": 1,
    "interaction_type": "bitbucket_pr_review",
    "occurred_at": "2025-10-24T11:30:00Z",
    "id": 2
  }
]
```

#### 4.2. 오류 (Error)

- **상태 코드:** `401 Unauthorized`
  - **원인:** 인증 토큰이 제공되지 않았거나 유효하지 않은 경우
- **상태 코드:** `403 Forbidden`
  - **원인:** 요청을 보낸 사용자가 관리자(`admin`) 권한을 가지고 있지 않은 경우
- **상태 코드:** `422 Unprocessable Entity`
  - **원인:** 요청 본문의 형식이 잘못된 경우 (예: 필수 필드 누락)
