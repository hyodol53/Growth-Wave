# API: GET /api/v1/projects/

## 1. 개요
사용자의 역할에 따라 접근 가능한 프로젝트 목록을 조회합니다.

- **Admin:** 시스템에 존재하는 모든 프로젝트 목록을 조회합니다.
- **실장 (Dept Head):** 자신의 하위 조직원이 PM(Project Manager)으로 할당된 모든 프로젝트 목록을 조회합니다.
- **그 외 역할:** 접근이 금지됩니다. (403 Forbidden)

## 2. 엔드포인트
`GET /api/v1/projects/`

## 3. 요청 (Request)
### 3.1. 헤더 (Headers)
- `Authorization`: `Bearer <JWT_TOKEN>` (필수)

## 4. 응답 (Response)
### 4.1. 성공 (200 OK)
프로젝트 정보 배열이 반환됩니다.
```json
[
  {
    "id": 1,
    "name": "Growth-Wave Development",
    "description": "Dual-track HR platform development project.",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "pm_id": 5,
    "pm": {
      "id": 5,
      "full_name": "PM User"
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
