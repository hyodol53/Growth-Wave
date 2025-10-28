# API: 내 하위 조직원 목록 조회

## `GET /api/v1/users/me/subordinates`

### 설명
현재 로그인한 사용자(팀장 또는 실장)의 모든 하위 조직원 목록을 조회합니다. 이 API는 정성평가 대상을 화면에 표시하기 위해 필요합니다.

### 접근 권한
- `team_lead`, `dept_head` 역할의 사용자만 접근 가능

### 요청 (Request)

- 별도의 요청 파라미터나 본문이 필요하지 않습니다.

### 응답 (Response)

#### 성공 (Success)
- **상태 코드:** `200 OK`
- **본문 (Body):** `User` 스키마의 배열

```json
[
  {
    "id": 15,
    "username": "subordinate1",
    "email": "sub1@example.com",
    "full_name": "나평가",
    "role": "employee",
    "organization_id": 10
  },
  {
    "id": 18,
    "username": "subordinate2",
    "email": "sub2@example.com",
    "full_name": "박직원",
    "role": "employee",
    "organization_id": 10
  }
]
```

#### 오류 (Error)
- **상태 코드:** `401 Unauthorized`
  - 인증되지 않은 사용자의 요청인 경우
- **상태 코드:** `403 Forbidden`
  - `team_lead` 또는 `dept_head`가 아닌 사용자가 요청한 경우
