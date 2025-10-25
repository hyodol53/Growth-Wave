# Task 4.2: 프로젝트 관리 기능 개발

`REQUIREMENTS.md`의 `FR-A-6.x` 요구사항에 따라, 실장 및 관리자가 프로젝트를 생성, 수정, 삭제하고 멤버를 배정할 수 있는 백엔드 기능을 개발했습니다.

## 1. 프로젝트 CRUD 기능 (FR-A-6.1)

- **API 엔드포인트 (`app/api/endpoints/projects.py`):**
    - `POST /api/v1/projects/`: 새로운 프로젝트를 생성합니다.
    - `GET /api/v1/projects/`: 모든 프로젝트 목록을 조회합니다.
    - `GET /api/v1/projects/{project_id}`: 특정 프로젝트의 정보를 조회합니다.
    - `PUT /api/v1/projects/{project_id}`: 프로젝트 정보를 수정합니다.
    - `DELETE /api/v1/projects/{project_id}`: 프로젝트를 삭제합니다.

- **권한 제어 (`app/api/deps.py`):**
    - 모든 생성, 수정, 삭제 엔드포인트는 `DEPT_HEAD` (실장) 또는 `ADMIN` (관리자) 역할만 접근할 수 있도록 `get_current_dept_head_user` 의존성을 사용했습니다.
    - 특히, 실장은 자신이 속한 부서(`organization`)의 프로젝트만 생성, 수정, 삭제할 수 있도록 API 레벨에서 소유권 검증 로직을 추가했습니다.

- **API 스키마 (`app/schemas/project.py`):**
    - `ProjectUpdate` 스키마의 모든 필드를 `Optional`로 변경하여, 부분적인 정보 수정(PATCH)이 가능하도록 유연성을 확보했습니다.

## 2. 프로젝트 멤버 배정 (FR-A-6.2)

- 프로젝트 멤버 배정 및 참여 비중 설정 기능은 Phase 2에서 구현된 `POST /api/v1/projects/members/weights` 엔드포인트를 그대로 활용합니다. 이번 Task에서는 프로젝트 자체의 CRUD 기능 구현에 집중했습니다.

## 3. 디버깅 및 안정화 과정

개발 및 테스트 과정에서 여러 오류가 발생했으며, 다음과 같이 해결했습니다.

- **`TypeError` in Tests:**
    - **원인:** `tests/api/test_projects.py`에서 사용하는 `create_random_organization` 및 `create_random_project` 테스트 유틸리티 함수들이 `name`과 같은 특정 인자를 받도록 설계되지 않았는데, 테스트 코드에서 이를 사용하려고 시도하여 발생했습니다.
    - **해결:** `tests/utils/organization.py`와 `tests/utils/project.py`의 해당 함수들을 수정하여, `name` 등의 인자를 선택적으로 받아 테스트 데이터 생성을 더 유연하게 할 수 있도록 개선했습니다.

- **`422 Unprocessable Entity` Error:**
    - **원인:** 프로젝트 수정(`PUT`) API 테스트에서 발생했으며, `ProjectUpdate` 스키마의 필드들이 `Optional`이 아니어서 요청 본문 데이터 유효성 검사에 실패했기 때문입니다.
    - **해결:** `app/schemas/project.py`의 `ProjectUpdate` 스키마 내 모든 필드를 `Optional`로 변경하여 문제를 해결했습니다.

- **`403 Forbidden` Error:**
    - **원인:** 관리자(`ADMIN`)가 프로젝트를 삭제하려 할 때 권한 오류가 발생했습니다. 이는 `get_current_dept_head_user` 의존성이 `DEPT_HEAD` 역할만 허용하고 `ADMIN`을 고려하지 않았기 때문입니다.
    - **해결:** `app/api/deps.py`의 `get_current_dept_head_user` 함수 로직을 수정하여 `ADMIN` 역할도 해당 엔드포인트에 접근할 수 있도록 허용했습니다.

위의 모든 문제 해결 과정을 거쳐, `poetry run pytest` 실행 시 모든 테스트(97개)가 성공적으로 통과하는 것을 확인하여 기능의 안정성을 확보했습니다.
