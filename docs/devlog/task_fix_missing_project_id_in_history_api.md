# Task: 사용자 이력 API에 `project_id` 추가

- **요구사항:** 프론트엔드에서 동료/PM 평가 대상자 목록을 가져오기 위해 `GET /projects/{project_id}/members` API를 호출해야 하지만, 기존 `GET /api/v1/users/me/history` API 응답에는 `project_id`가 없어 호출이 불가능한 문제 발생.
- **작업 목표:** `GET /api/v1/users/me/history` 및 `GET /api/v1/users/{user_id}/history` API의 응답에 `project_id`를 포함하여 프론트엔드 개발을 원활하게 지원한다.

## 작업 내역

1.  **스키마 수정 (`app/schemas/user.py`):**
    -   `ProjectHistoryItem` Pydantic 스키마에 `project_id: int` 필드를 추가하여 API 응답 모델을 갱신했습니다.

2.  **CRUD 로직 수정 (`app/crud/user.py`):**
    -   `get_user_history` 함수 내에서 `ProjectHistoryItem` 객체를 생성할 때, `pm.project.id` 값을 `project_id` 필드에 할당하도록 수정했습니다. 이로써 데이터베이스 조회 결과가 API 응답에 올바르게 포함되도록 했습니다.

3.  **테스트 코드 수정 (`tests/api/test_users.py`):**
    -   `test_read_my_history` 테스트 케이스에 `project_id`가 응답에 올바르게 포함되었는지 확인하는 단언(`assert`)을 추가하여 변경 사항을 검증하고 API의 안정성을 확보했습니다.

## 결과

-   `poetry run pytest`를 실행하여 전체 105개 테스트가 모두 통과하는 것을 확인했습니다.
-   이제 프론트엔드에서는 사용자 이력 API를 통해 각 프로젝트의 `project_id`를 정상적으로 얻을 수 있습니다.
