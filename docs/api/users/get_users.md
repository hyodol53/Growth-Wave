# API: GET /api/v1/users/

## 1. 개요
역할 기반으로 사용자 목록을 조회합니다.

- **Admin:** 시스템의 모든 사용자 목록을 조회합니다.
- **실장 (Dept Head):** 자신의 하위 조직에 속한 모든 사용자 목록을 조회합니다.
- **그 외 역할:** 접근이 금지됩니다. (403 Forbidden)

## 2. 엔드포인트
`GET /api/v1/users/`

## 3. 요청 (Request)
### 3.1. 헤더 (Headers)
- `Authorization`: `Bearer <JWT_TOKEN>` (필수)

## 4. 응답 (Response)
### 4.1. 성공 (200 OK)
사용자 정보 배열이 반환됩니다.
```json
[
  {
    "id": 1,
    "username": "admin_user",
    "full_name": "Admin User",
    "email": "admin@example.com",
    "role": "admin",
    "organization_id": null,
    "organization": null
  },
  {
    "id": 2,
    "username": "dept_head_user",
    "full_name": "Dept Head User",
    "email": "head@example.com",
    "role": "dept_head",
    "organization_id": 1,
    "organization": {
        "id": 1,
        "name": "Core Tech Department",
        "level": 2,
        "parent_id": null
    }
  }
]
```

### 4.2. 실패
- **401 Unauthorized:** 인증되지 않은 사용자의 요청일 경우
- **403 Forbidden:** 권한이 없는 역할(예: `team_lead`, `employee`)의 사용자가 요청할 경우

## 5. 권한 (Authorization)
- `admin`
- `dept_head`
