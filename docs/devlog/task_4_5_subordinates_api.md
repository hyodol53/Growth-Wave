# 개발 로그: Task 4.5 - 하위 조직원 조회 API 개발

**담당자:** Agent-Backend
**상태:** 완료

## 1. 작업 목표
- `WORK_PLAN.md`의 Task 4.5에 따라, 현재 로그인한 관리자(팀장 또는 실장)의 모든 하위 조직원 목록을 조회하는 `GET /api/v1/users/me/subordinates` API를 구현한다.
- API 명세는 `docs/api/users/get_my_subordinates.md`를 따른다.

## 2. 개발 과정

### 2.1. CRUD 함수 분석 및 활용
- `app/crud/user.py` 파일을 분석한 결과, `get_subordinates`라는 이름의 CRUD 함수가 이미 구현되어 있음을 확인했다.
- 이 함수는 주어진 `user_id`를 기반으로 해당 사용자의 조직 및 모든 하위 조직에 속한 사용자들을 조회하고, 요청한 사용자 자신은 결과에서 제외하는 로직을 포함하고 있었다.
- 따라서 별도의 새로운 CRUD 함수를 작성할 필요 없이 기존 함수를 활용하기로 결정했다.
- 초기에는 `app/crud/organization.py`에 하위 조직 ID를 재귀적으로 가져오는 헬퍼 함수(`get_descendant_org_ids`)를 추가하려 했으나, `user_crud.user.get_subordinates` 함수가 이미 `crud_org.get_all_descendant_orgs`를 사용하여 필요한 로직을 처리하고 있음을 확인하고 해당 변경 사항을 되돌렸다.

### 2.2. API 엔드포인트 추가
- `app/api/endpoints/users.py`에 `GET /me/subordinates` 라우터를 추가했다.
- 이 엔드포인트는 다음 로직을 수행한다:
    1. 현재 로그인한 사용자의 역할(`current_user.role`)이 `team_lead` 또는 `dept_head`인지 확인한다. 해당 역할이 아니면 `403 Forbidden` 오류를 반환하여 접근 권한을 제어한다.
    2. `user_crud.user.get_subordinates` 함수를 호출하여 현재 관리자의 하위 조직원 목록을 가져온다.
    3. 조회된 하위 조직원 목록을 `User` 스키마의 배열 형태로 응답한다.

### 2.3. 테스트 코드 작성
- `tests/api/test_users.py`에 신규 API에 대한 포괄적인 테스트 케이스를 추가했다.
- **`test_read_my_subordinates_as_dept_head`**: 실장(dept_head)이 자신의 하위 조직(실, 팀)에 속한 모든 구성원(팀장, 직원)을 올바르게 조회하는지 검증한다. 자신과 다른 부서의 직원은 포함되지 않음을 확인한다.
- **`test_read_my_subordinates_as_team_lead`**: 팀장(team_lead)이 자신의 하위 조직(팀)에 속한 직원만 올바르게 조회하는지 검증한다.
- **`test_read_my_subordinates_as_employee`**: 일반 직원(employee)이 해당 API에 접근했을 때, 권한 부족으로 `403 Forbidden` 오류가 발생하는지 검증한다.

## 3. 최종 확인
- 전체 테스트(`poetry run pytest`)를 실행하여 105개의 모든 테스트가 통과하는 것을 확인했다.
