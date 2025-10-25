# Task 4.3: 평가 및 프로젝트 이력 조회 기능 개발

`REQUIREMENTS.md`의 `FR-A-5.4` 요구사항에 따라, 구성원과 보직자가 반기별로 자신의 프로젝트 진행 이력과 평가 결과를 조회할 수 있는 API를 개발했습니다.

## 1. 핵심 기능

- **API 엔드포인트:**
    - `GET /api/v1/users/me/history`: 현재 로그인한 사용자가 자신의 과거 평가 및 프로젝트 이력을 조회합니다.
    - `GET /api/v1/users/{user_id}/history`: 보직자(`dept_head`, `admin`)가 자신의 하위 조직원 또는 특정 사용자의 이력을 조회합니다.

- **데이터 모델 확장:**
    - `app/models/project.py`의 `Project` 모델에 `start_date`와 `end_date` 컬럼을 추가하여 프로젝트의 유효 기간을 기록할 수 있도록 했습니다. 이는 특정 평가 기간 내에 수행된 프로젝트를 필터링하는 데 핵심적인 역할을 합니다.

- **계층적 데이터 스키마 (`app/schemas/user.py`):**
    - 이력 조회를 위한 `UserHistoryResponse`, `UserHistoryEntry`, `ProjectHistoryItem` Pydantic 스키마를 새로 정의했습니다.
    - 이 스키마들은 `[평가 기간 -> {평가 결과, [프로젝트 참여 내역]}]` 형태의 중첩된 구조로, 사용자의 반기별 이력을 명확하게 표현합니다.

- **CRUD 로직 구현 (`app/crud/user.py`, `app/crud/project_member.py`):**
    - `user.py`에 `get_user_history` 함수를 구현하여, 모든 평가 기간을 순회하며 각 기간에 해당하는 최종 평가(FinalEvaluation)와 프로젝트 참여 기록을 조합하는 핵심 비즈니스 로직을 담당합니다.
    - `project_member.py`에는 `get_multi_by_user_and_period` 함수를 새로 추가하여, 특정 사용자가 주어진 기간 내에 참여한 프로젝트 목록을 효율적으로 조회할 수 있도록 했습니다.

- **권한 제어 (`app/api/endpoints/users.py`):**
    - `/me/history`는 `get_current_user` 의존성을 통해 본인만 접근 가능하도록 제한했습니다.
    - `/{user_id}/history`는 `get_user_as_subordinate` 의존성을 사용하여 관리자 또는 해당 유저의 상위 보직자만 접근할 수 있도록 엄격하게 권한을 제어합니다.

## 2. 디버깅 및 안정화 과정

개발 및 테스트 과정에서 `ImportError`, `TypeError`, `AttributeError` 등 다양한 오류가 발생했으며, 다음과 같이 해결했습니다.

- **`ImportError`:**
    - **원인:** `tests/api/test_users.py`에서 `create_random_evaluation_period`와 같은 테스트 유틸리티 함수를 임포트하려 했으나, 해당 함수가 `tests/utils/evaluation.py`에 존재하지 않아 발생했습니다.
    - **해결:** `tests/utils/evaluation.py` 파일에 누락된 `create_random_evaluation_period` 함수를 추가하고, 중복 정의된 다른 함수들을 정리했습니다.

- **`TypeError`:**
    - **원인:** `Project` 모델 및 스키마에 `start_date`, `end_date` 필드를 추가한 후, 테스트 유틸리티 함수인 `create_random_project`가 이 인자들을 받도록 업데이트하는 것을 누락하여 발생했습니다. 또한, `create_random_final_evaluation` 호출 시 필수 인자인 `final_score`를 전달하지 않아 오류가 발생했습니다.
    - **해결:** `tests/utils/project.py`의 `create_random_project` 함수 시그니처에 `start_date`, `end_date`를 추가하고, `tests/api/test_users.py`에서 `create_random_final_evaluation` 호출 시 `final_score` 값을 명시적으로 전달하도록 수정했습니다.

- **`AttributeError`:**
    - **원인:** 테스트 유틸리티 함수 내에서 CRUD 객체의 메소드를 잘못 호출(예: `crud.final_evaluation.final_evaluation.create` 대신 `crud.final_evaluation.create`가 올바른 호출)하여 발생했습니다.
    - **해결:** `app/crud/__init__.py`의 구조를 확인하고, `tests/utils/evaluation.py` 내의 모든 CRUD 메소드 호출을 올바른 방식으로 수정했습니다.

- **구조적 오류:**
    - **원인:** `app/crud/user.py` 파일에서 `get_user_history` 함수가 `get_subordinates` 함수 내부에 잘못된 들여쓰기로 정의되어 있었습니다.
    - **해결:** 파일의 전체적인 공백과 들여쓰기를 수정하여 `get_user_history`를 `CRUDUser` 클래스의 독립적인 메소드로 바로잡았습니다.

위의 모든 문제 해결 과정을 거쳐, `poetry run pytest` 실행 시 모든 테스트(100개)가 성공적으로 통과하는 것을 확인하여 기능의 안정성을 확보했습니다.
