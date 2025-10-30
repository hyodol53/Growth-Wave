# 개발 로그: 평가 기간-프로젝트 관계 재정립

- **날짜:** 2025년 10월 30일
- **담당자:** 백엔드 에이전트
- **관련 문서:**
    - `docs/request_for_backend_refactor_project_evaluation_period.md`
    - `docs/api/projects/create_project.md`
    - `docs/api/projects/get_projects.md`

## 1. 작업 요약

프론트엔드 팀의 요청에 따라, 기존에 날짜 범위를 통해 암묵적으로 연결되었던 '프로젝트'와 '평가 기간'의 관계를 명확하게 재정립했습니다. 이제 모든 프로젝트는 생성 시점에 특정 `evaluation_period_id`를 외래 키로 가지며, 명시적으로 하나의 평가 기간에 귀속됩니다.

이 변경 사항을 반영하여 신규 프로젝트 생성 및 조회 API를 구현하고, 관련된 모든 데이터베이스 모델, 스키마, CRUD 함수, 그리고 테스트 코드를 수정했습니다.

## 2. 주요 변경 사항

### 2.1. 데이터베이스 모델 변경 (`app/models/`)

- **`project.py`:**
    - `evaluation_period_id` 컬럼(Integer, ForeignKey)을 추가하여 `evaluation_periods` 테이블과 직접적인 관계를 설정했습니다. (`nullable=False`)
    - 기존의 `description` 필드를 삭제하고, `name` 필드의 `unique` 제약조건을 제거했습니다.
- **`evaluation.py`:**
    - `EvaluationPeriod` 모델에 `projects` 관계(back-populates)를 추가하여 양방향 관계를 완성했습니다.

### 2.2. API 스키마 추가 (`app/schemas/project.py`)

- `ProjectCreate`, `ProjectUpdate`, `Project` 등 프로젝트 API의 요청 및 응답 본문을 처리하기 위한 Pydantic 스키마를 새로 정의했습니다.
- 모든 스키마는 `evaluation_period_id` 필드를 포함하도록 작성되었습니다.

### 2.3. CRUD 로직 추가 및 수정 (`app/crud/`)

- **`crud_project.py`:**
    - 프로젝트 생성을 위한 기본 CRUD 로직과 더불어, `get_multi_by_filter` 함수를 새로 구현했습니다.
    - 이 함수는 `evaluation_period_id`, `pm_id`, `user_id` 등 다양한 쿼리 파라미터를 기반으로 프로젝트 목록을 필터링하는 기능을 제공합니다.
- **`project_member.py`:**
    - 날짜 범위 대신 `evaluation_period_id`를 기준으로 사용자의 프로젝트 참여 이력을 조회하는 `get_multi_by_user_and_evaluation_period` 함수를 새로 추가했습니다.
- **`user.py`:**
    - `get_user_history` 함수가 `get_multi_by_user_and_evaluation_period`를 사용하도록 수정하여, 사용자 이력 조회 시 명시적인 ID를 통해 프로젝트를 가져오도록 변경했습니다.

### 2.4. API 엔드포인트 구현 (`app/api/endpoints/projects.py`)

- API 명세에 따라 다음 두 개의 엔드포인트를 새로 구현하고, 메인 라우터에 등록했습니다.
    - **`POST /api/v1/projects`:**
        - `evaluation_period_id`를 포함한 요청을 받아 새 프로젝트를 생성합니다.
        - `deps.get_current_admin_or_dept_head_user` 의존성을 사용하여 실장급 이상 관리자만 접근할 수 있도록 권한을 제어합니다.
    - **`GET /api/v1/projects`:**
        - `evaluation_period_id` 등 다양한 조건으로 프로젝트 목록을 조회합니다.

### 2.5. 테스트 코드 전면 리팩토링 (`tests/`)

데이터 모델의 핵심적인 변경으로 인해 다수의 테스트 코드가 실패했으며, 이를 해결하기 위해 다음과 같이 광범위한 리팩토링을 진행했습니다.

- **`tests/api/test_projects.py`:**
    - 기존 테스트를 모두 삭제하고, 새로운 API 명세(`POST /projects`, `GET /projects`)에 맞는 테스트 케이스를 재작성했습니다.
    - `evaluation_period_id` 필터링 기능이 올바르게 동작하는지 검증하는 테스트를 추가했습니다.
- **테스트 유틸리티 수정 및 추가:**
    - **`tests/utils/project.py`:** `create_random_project` 함수가 내부적으로 `evaluation_period`를 생성하거나 `evaluation_period_id`를 인자로 받을 수 있도록 수정하여, 다른 테스트 코드에 미치는 영향을 최소화했습니다.
    - **`tests/utils/evaluation_period.py`:** 테스트 중 고유한 이름의 평가 기간을 생성하는 헬퍼 함수를 추가했습니다.
    - **`tests/utils/common.py`:** `random_lower_string`과 같은 공통 유틸리티 함수를 위한 파일을 새로 생성했습니다.
- **기존 테스트 파일 수정:**
    - `create_random_project`를 사용하는 모든 테스트 파일(`test_pm_evaluations.py`, `test_project_members.py`, `test_users.py` 등)에서 발생하는 오류를 해결하고, 변경된 로직에 맞게 단언문을 수정했습니다.
    - 더 이상 존재하지 않는 API(`POST /projects/{id}/members`)를 테스트하는 코드는 주석 처리했습니다.

## 3. 결과

- 프로젝트와 평가 기간의 관계 재정립 작업이 성공적으로 완료되었습니다.
- 신규 API가 명세에 맞게 구현되었으며, 관련된 모든 테스트가 통과하는 것을 확인했습니다.
- 이제 프론트엔드 팀은 `evaluation_period_id`를 기준으로 프로젝트를 생성하고 조회할 수 있습니다.
