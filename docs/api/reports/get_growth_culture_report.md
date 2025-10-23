# API: Growth & Culture 리포트 조회

- **HTTP Method:** `GET`
- **URL:** `/api/v1/users/{user_id}/growth-culture-report`

## 설명

요구사항 명세서의 `FR-A-4.6`에 따라, 특정 사용자의 'Growth & Culture 리포트'를 조회합니다. 이 리포트는 관리자(실장급 이상)가 정성평가, 등급 조정, 동점자 처리 등 주관적 판단을 내릴 때 참고 자료로 사용됩니다.

현재 버전에서는 '강점 프로필 요약' 정보를 제공합니다. '협업 네트워크 요약'은 향후 구현될 예정입니다.

## 접근 권한

- `ADMIN` 또는 `DEPT_HEAD` 역할을 가진 사용자만 접근할 수 있습니다.
- `DEPT_HEAD` 역할의 사용자는 자신의 하위 조직(자신이 속한 조직 및 모든 하위 조직)에 속한 구성원의 리포트만 조회할 수 있습니다.

## 요청 (Request)

### URL 파라미터

- `user_id` (integer, required): 리포트를 조회할 대상 사용자의 ID

## 응답 (Response)

### 성공 (200 OK)

```json
{
  "strength_profile": {
    "user_id": 1,
    "full_name": "이성장",
    "total_praises": 5,
    "strengths": [
      {
        "hashtag": "#teamwork",
        "count": 3
      },
      {
        "hashtag": "#communication",
        "count": 2
      }
    ]
  },
  "collaboration_summary": {
    "message": "This feature will be implemented in the future."
  }
}
```

### 주요 오류

- **403 Forbidden:**
  - 요청자가 리포트를 조회할 권한이 없는 경우 (`detail`: "You do not have enough privileges for this operation.")
  - `DEPT_HEAD`가 자신의 하위 조직원이 아닌 사용자의 리포트를 조회하려고 시도하는 경우 (`detail`: "You can only view reports for users in your department.")
- **404 Not Found:**
  - `user_id`에 해당하는 사용자가 존재하지 않는 경우 (`detail`: "User not found")
