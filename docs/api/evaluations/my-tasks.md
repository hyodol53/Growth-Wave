# `GET /api/v1/evaluations/my-tasks`

## 1. 개요

현재 로그인한 사용자가 활성 평가 기간 내에 평가해야 하는 모든 프로젝트 목록을 조회합니다. 프론트엔드에서 '내 평가' 페이지의 프로젝트 선택 드롭다운 메뉴를 구성하는 데 사용됩니다.

## 2. 요청

### 2.1. Headers

| Key | Value | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `Authorization` | `Bearer <JWT_TOKEN>` | O | 사용자의 JWT Access Token |

## 3. 응답

### 3.1. 성공 (200 OK)

**Content-Type:** `application/json`

```json
[
  {
    "project_id": 1,
    "project_name": "Growth-Wave 개발",
    "user_role_in_project": "PM"
  },
  {
    "project_id": 2,
    "project_name": "신규 서비스 기획",
    "user_role_in_project": "MEMBER"
  }
]
```

- **활성 평가 기간이 없는 경우, 빈 배열(`[]`)을 반환합니다.**

### 3.2. 실패

- **401 Unauthorized**: 인증 토큰이 유효하지 않은 경우
