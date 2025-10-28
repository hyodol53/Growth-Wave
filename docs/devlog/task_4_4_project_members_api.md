# 개발 로그: Task 4.4 - 프로젝트 멤버 조회 API 개발

**담당자:** Agent-Backend
**상태:** 완료

## 1. 작업 목표
- `WORK_PLAN.md`의 Task 4.4에 따라, 프론트엔드에서 동료평가 대상자를 표시하는 데 필요한 `GET /api/v1/projects/{project_id}/members` API를 구현한다.
- API 명세는 `docs/api/projects/get_project_members.md`를 따른다.

## 2. 개발 과정

### 2.1. 응답 스키마 정의
- API 명세의 응답 형식에 따라 `user_id`, `full_name`, `is_pm`, `participation_weight` 필드를 포함하는 `ProjectMemberDetail` Pydantic 스키마를 `app/schemas/project_member.py`에 추가했다.

### 2.2. CRUD 함수 작성
- `app/crud/project_member.py`에 `get_multi_by_project_with_user_details` 함수를 추가했다.
- 이 함수는 `ProjectMember` 테이블과 `User` 테이블을 조인하여, 특정 프로젝트에 속한 멤버들의 상세 정보(특히 `full_name`)를 한 번의 쿼리로 가져오도록 구현했다.
- SQLAlchemy의 `label()`을 사용하여 조회된 각 컬럼에 명시적인 이름을 부여함으로써, API 엔드포인트에서 데이터를 안전하고 명확하게 처리할 수 있도록 했다.

### 2.3. API 엔드포인트 추가
- `app/api/endpoints/projects.py`에 `GET /{project_id}/members` 라우터를 추가했다.
- 이 엔드포인트는 다음 로직을 수행한다:
    1. 요청된 `project_id`에 해당하는 프로젝트가 존재하는지 확인하고, 없으면 `404 Not Found` 오류를 반환한다.
    2. 위에서 작성한 `get_multi_by_project_with_user_details` CRUD 함수를 호출한다.
    3. 반환된 데이터를 `ProjectMemberDetail` 스키마 목록에 맞게 매핑하여 응답한다.

### 2.4. 테스트 코드 작성
- `tests/api/test_projects.py`에 신규 API에 대한 테스트 케이스를 추가했다.
- **`test_read_project_members`**: 특정 프로젝트에 멤버를 추가하고 API를 호출했을 때, 상태 코드 200과 함께 정확한 멤버 목록이 반환되는지 검증한다.
- **`test_read_project_members_not_found`**: 존재하지 않는 프로젝트 ID로 요청 시, 상태 코드 404가 반환되는지 검증한다.

## 3. 문제 해결
- 초기 테스트 작성 시, 테스트 유틸리티 함수인 `create_random_user`에 `full_name` 인자를 직접 전달하여 `TypeError`가 발생했다.
- `create_random_user` 함수를 수정하는 대신, 테스트 코드 내에서 해당 함수가 랜덤하게 생성한 `full_name` 값을 그대로 가져와 API 응답값과 비교하는 방식으로 수정하여 문제를 해결했다. 이 방법은 다른 테스트에 영향을 주지 않는 더 안전한 접근 방식이다.

## 4. 최종 확인
- 전체 테스트(`poetry run pytest`)를 실행하여 105개의 모든 테스트가 통과하는 것을 확인했다.
