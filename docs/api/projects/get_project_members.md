# API: 프로젝트 멤버 목록 조회

## `GET /api/v1/projects/{project_id}/members`

### 설명
특정 프로젝트에 속한 모든 멤버의 목록과 정보를 조회합니다. 이 API는 동료평가 또는 PM평가 대상을 화면에 표시하기 위해 필요합니다.

### 접근 권한
- 인증된 모든 사용자 (`employee`, `team_lead`, `dept_head`, `admin`)

### 요청 (Request)

#### 경로 파라미터 (Path Parameters)
- `project_id` (integer, required): 멤버 목록을 조회할 프로젝트의 ID

### 응답 (Response)

#### 성공 (Success)
- **상태 코드:** `200 OK`
- **본문 (Body):** `ProjectMemberDetail` 스키마의 배열

```json
[
  {
    "user_id": 2,
    "full_name": "홍길동",
    "is_pm": true,
    "participation_weight": 50
  },
  {
    "user_id": 5,
    "full_name": "김철수",
    "is_pm": false,
    "participation_weight": 50
  }
]
```

#### 오류 (Error)
- **상태 코드:** `401 Unauthorized`
  - 인증되지 않은 사용자의 요청인 경우
- **상태 코드:** `404 Not Found`
  - `project_id`에 해당하는 프로젝트가 존재하지 않는 경우
