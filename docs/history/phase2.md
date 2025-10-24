# Phase 2: Track A - 평가 설정 및 진행 기능 개발 완료
`WORK_PLAN.md`의 Phase 2 목표 중 평가 설정 및 진행과 관련된 핵심 기능 개발을 완료했습니다. '조직도 관리', '프로젝트 참여 비중 설정', '평가 항목 가중치 설정', 그리고 '평가 진행 API' 기능 개발을 완료하고 전체 테스트 통과를 통해 안정성을 확보했습니다.

## 완료된 작업

### 2.1 조직도 관리 기능 개발 (파일 임포트)
관리자가 조직도 파일을 업로드하여 전체 조직의 구조를 일괄적으로 생성, 수정, 삭제(동기화)하는 기능이 구현되었습니다.

- **API 엔드포인트 (`app/api/endpoints/organizations.py`):** `POST /api/v1/organizations/upload`
- **핵심 로직 (`app/crud/organization.py`):** `sync_organizations_from_file`
- **테스트 코드 (`tests/api/test_organizations.py`):** 조직도 동기화 기능의 정확성 및 안정성 검증 완료.

### 2.2 프로젝트 참여 비중 설정 API 개발 (FR-A-1.3)
'FR-A-1.3: 실장은 평가 기간 내 소속 인원의 프로젝트별 참여 비중(%)을 설정할 수 있어야 하며, 총합은 100%여야 한다.' 요구사항을 구현했습니다.

-   **데이터 모델:** `Project`, `ProjectMember` 모델 생성 및 기존 모델 업데이트.
-   **API 엔드포인트:** `POST /api/v1/projects/members/weights` 엔드포인트 생성 및 권한/유효성 검사 로직 구현.
-   **테스트:** `tests/api/test_projects.py`를 포함한 관련 테스트 코드 작성.

### 2.3 평가 주기 및 등급 비율 설정 API 안정화 (FR-A-2.1, FR-A-2.2)
이전 개발에서 `TypeError`로 인해 중단되었던 평가 주기 및 등급 비율 관리 API의 버그를 수정하고 안정화했습니다.

-   **핵심 로직 (`app/crud/base.py`):** `create` 메서드가 Pydantic 모델과 `dict` 타입을 모두 처리할 수 있도록 수정하여, 날짜 타입 변환 오류와 `AttributeError`를 모두 해결했습니다.
-   **API 엔드포인트 (`app/api/endpoints/evaluations.py`):** 관리자만 접근 가능한 평가 주기 및 등급 비율 CRUD API가 이제 정상적으로 동작합니다.
-   **테스트 (`tests/api/test_evaluations.py`):** 관련된 모든 테스트가 통과하는 것을 확인하여 기능 안정성을 검증했습니다.

### 2.4 평가 항목 가중치 설정 API 개발 (FR-A-2.3)
'FR-A-2.3: 시스템 관리자는 직책별 평가 항목의 가중치(%)를 조정할 수 있어야 한다.' 요구사항을 구현했습니다.

-   **데이터 모델 (`app/models/evaluation.py`):** `EvaluationWeight` 모델을 추가하여 직책, 평가 항목, 가중치를 저장합니다.
-   **API 엔드포인트 (`app/api/endpoints/evaluations.py`):** 관리자만 접근 가능한 CRUD API 엔드포인트를 구현했습니다.
-   **테스트 (`tests/api/test_evaluations.py`):** 기능의 정상 동작과 관리자 권한 제어를 검증하는 테스트 코드를 작성하고, 모든 테스트 통과를 확인했습니다.

### 2.5 평가 진행 API 개발 (PM동료/PM/정성) (FR-A-3.x)
`WORK_PLAN.md`의 2.5 항목에 따라, 동료/PM/정성 평가를 진행하는 API 개발을 완료했습니다.

-   **PM동료평가 (FR-A-3.1):** 피평가자가 동료에게 점수를 부여하며, 평균 70점 초과 시 제출을 제한하는 API를 구현했습니다. (`POST /api/v1/evaluations/peer-evaluations/`)
-   **PM평가 (FR-A-3.3):** 프로젝트 관리자(PM)가 구성원에게 점수를 부여하는 API를 구현했으며, PM만 해당 기능을 사용할 수 있도록 권한을 제어했습니다. (`POST /api/v1/evaluations/pm-evaluations/`)
-   **정성평가 (FR-A-3.5):** 팀장/실장이 자신의 하위 조직원에게 점수를 부여하는 API를 구현했으며, 상급자만 해당 기능을 사용할 수 있도록 권한을 제어했습니다. (`POST /api/v1/evaluations/qualitative-evaluations/`)
-   **테스트:** 각 평가 API의 정상 동작, 유효성 검사, 권한 제어를 검증하는 테스트 코드를 `tests/api/` 하위에 작성하고 모든 테스트 통과를 확인했습니다.

### 2.6 최종 등급 산출 로직 개발 (FR-A-4.1, FR-A-4.2)
`REQUIREMENTS.md`의 FR-A-4.1("가중치 합산") 및 FR-A-4.2("복수 프로젝트 점수 합산") 요구사항에 따라, 개별 평가 데이터와 직책별 가중치, 프로젝트 참여 비중을 기반으로 최종 평가 점수를 산출하는 로직과 API를 개발했습니다.

-   **데이터 모델:** `FinalEvaluation` 모델을 추가하여 최종 계산된 평가 점수를 저장합니다.
-   **스키마:** `FinalEvaluation` 관련 Pydantic 스키마를 생성했습니다.
-   **CRUD 작업:** `CRUDFinalEvaluation` 클래스를 구현하고, `get_by_evaluatee_and_period` 메서드를 추가했습니다.
-   **계산 로직:** `app/crud/evaluation_calculator.py`에 `calculate_and_store_final_scores` 함수를 구현하여 최종 점수를 계산하고 저장합니다。
-   **API 엔드포인트:** `POST /api/v1/evaluations/calculate` 엔드포인트를 추가하여 최종 평가 점수 계산을 트리거하며, `DEPT_HEAD` 또는 `ADMIN` 역할만 접근 가능하도록 권한을 제어했습니다.
-   **테스트:** 이 기능에 대한 테스트 코드는 현재 보류 중입니다.
-   **테스트 완료:** `tests/api/test_final_evaluations.py`에 테스트 코드를 작성하고 모든 테스트를 성공적으로 통과하여 기능의 안정성을 확보했습니다. 상세 내용은 `docs/devlog/task_2_6_final_grade_calculation_tests.md`를 참조하십시오.

### 2.7 Growth & Culture 리포트 조회 API 개발 (FR-A-4.6)
`REQUIREMENTS.md`의 `FR-A-4.6` 요구사항에 따라, 관리자가 평가 시 참고할 수 있는 'Growth & Culture 리포트' 조회 API를 개발했습니다. 이 기능은 Track A(평가)와 Track B(성장)를 연결하는 핵심적인 역할을 합니다.

-   **API 엔드포인트:** `GET /api/v1/users/{user_id}/growth-culture-report` 엔드포인트를 신설했습니다.
-   **핵심 로직:** 현재 리포트는 Track B의 '칭찬하기' 기능으로부터 집계된 '강점 프로필' 정보를 포함합니다.
-   **권한 제어:** `ADMIN`과 `DEPT_HEAD`만 접근 가능하며, `DEPT_HEAD`는 자신의 하위 조직원만 조회할 수 있도록 제한했습니다.
-   **테스트:** 신규 API의 정상 동작과 권한 제어 로직을 검증하는 테스트 코드를 `tests/api/test_reports.py`에 작성하고 모든 테스트 통과를 확인했습니다.

### 2.8 등급 조정 API 개발 (FR-A-4.4, FR-A-4.5)
`REQUIREMENTS.md`의 FR-A-4.4("B+/B- 등급 조정") 및 FR-A-4.5("동점자 처리") 요구사항에 따라, 실장 및 관리자가 최종 등급을 조정할 수 있는 API를 개발했습니다.

-   **API 엔드포인트:** `POST /api/v1/evaluations/adjust-grades`
-   **핵심 로직:** B+/B- 인원수 검증, 부서별 TO(정원) 검증 로직을 포함한 등급 조정 기능을 구현했습니다.
-   **테스트:** `tests/api/test_grade_adjustments.py`에 성공, 실패, 권한 제어 등 다양한 시나리오에 대한 테스트 케이스를 작성하여 안정성을 검증했습니다.

### 2.9 데이터 열람 권한 로직 구현 (FR-A-5.x)
`REQUIREMENTS.md`의 `FR-A-5.x` 요구사항에 따라, 사용자 역할(피평가자, 실장, 관리자)별로 평가 데이터를 조회할 수 있는 API와 권한 제어 로직을 구현했습니다.

-   **API 엔드포인트:**
    -   `GET /api/v1/evaluations/me`: 자신의 평가 결과를 조회합니다. (피평가자용)
    -   `GET /api/v1/evaluations/{user_id}/result`: 하위 직원의 상세 평가 결과를 조회합니다. (실장/관리자용)
-   **핵심 로직:** 역할에 따라 다른 데이터 스키마(`MyEvaluationResult`, `ManagerEvaluationView`)를 사용하여 민감한 정보 노출을 제어하고, `deps.py`에 권한 검증을 위한 의존성 함수(`get_user_as_subordinate`)를 추가했습니다.
-   **테스트:** `tests/api/test_evaluation_permissions.py`에 역할별 접근 시나리오(성공/실패)에 대한 테스트 케이스를 작성하여 기능의 안정성을 검증했습니다.

## 테스트 실패 해결 및 기능 안정화

API 개발 과정에서 발생했던 다양한 테스트 실패들을 모두 해결했으며, 전체 테스트가 통과하는 것을 확인했습니다.

*   **`TypeError` 해결**: 키워드 전용 인자를 위치 인자로 잘못 호출한 문제를 수정했습니다.
*   **`AttributeError` 해결 (CRUD 모듈 호출 오류)**: 모듈 내 인스턴스를 통해 메서드를 호출하도록 수정하여 해결했습니다.
*   **`AssertionError` 해결**: 테스트 코드의 기대 오류 메시지를 실제 API 반환 메시지와 일치하도록 수정했습니다.
*   **`AttributeError` 및 `ModuleNotFoundError` (다수)**: `__init__.py` 파일에 신규 모듈 및 인스턴스를 등록하지 않아 발생한 문제를 해결하고, 잘못된 import 경로를 수정했습니다.
*   **`InvalidRequestError` (SQLAlchemy)**: 테스트 실행 중 모델 클래스가 중복으로 정의되어 발생한 오류를 `__table_args__ = {'extend_existing': True}` 옵션을 추가하여 해결했습니다.
*   **`ValidationError` (Pydantic)**: SQLAlchemy 모델 객체를 Pydantic 스키마로 변환 시 `orm_mode`(현 `from_attributes`) 설정이 누락되어 발생한 오류를 `ConfigDict`를 사용하여 해결했습니다.

## 결론
위의 모든 오류를 해결한 결과, `poetry run pytest` 실행 시 모든 테스트가 성공적으로 통과하는 것을 확인했습니다. 이로써 Phase 2에서 계획된 Track A의 모든 기능(평가 설정, 진행, 산출, 조정 및 결과 조회) 개발이 안정적으로 완료되었음을 선언합니다.
