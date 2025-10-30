# API: 특정 평가 기간의 평가 완료 사용자 목록 조회

## `GET /api/v1/evaluations/periods/{period_id}/evaluated-users`

### 1. 개요

특정 평가 기간(`period_id`)에 대해 최종 평가가 생성된 사용자 목록을 조회합니다. 관리자 또는 실장이 평가 결과를 조회할 대상 인원을 선택하는 화면을 구성하는 데 사용됩니다.

### 2. 접근 권한

-   `DEPT_HEAD` (실장)
-   `ADMIN` (관리자)

### 3. 요청 (Request)

#### 3.1. 경로 파라미터 (Path Parameters)

| 이름 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `period_id` | `integer` | Y | 조회할 평가 기간의 ID |

#### 3.2. 헤더 (Headers)

| 이름 | 값 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `Authorization` | `Bearer <JWT_TOKEN>` | Y | 사용자의 JWT Access Token |

### 4. 응답 (Response)

#### 4.1. 성공 (200 OK)

**Content-Type:** `application/json`

-   `DEPT_HEAD`의 경우, 자신의 하위 조직에 속한 사용자 중 평가가 완료된 인원만 반환됩니다.
-   `ADMIN`의 경우, 전체 사용자 중 평가가 완료된 인원이 반환됩니다.

```json
[
  {
    "user_id": 1,
    "full_name": "김직원",
    "title": "선임연구원",
    "organization_name": "플랫폼개발팀"
  },
  {
    "user_id": 5,
    "full_name": "박팀장",
    "title": "팀장",
    "organization_name": "플랫폼개발팀"
  }
]
```

#### 4.2. 실패 (Failure)

-   **401 Unauthorized**: 인증 토큰이 유효하지 않은 경우
-   **403 Forbidden**: 요청을 보낸 사용자가 `DEPT_HEAD` 또는 `ADMIN` 권한을 가지고 있지 않은 경우
-   **404 Not Found**: 해당 `period_id`를 가진 평가 기간이 존재하지 않는 경우
