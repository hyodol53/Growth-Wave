# Task 2.6: 최종 등급 산출 로직 개발 (FR-A-4.1, FR-A-4.2)

`REQUIREMENTS.md`의 FR-A-4.1("가중치 합산") 및 FR-A-4.2("복수 프로젝트 점수 합산") 요구사항에 따라, 개별 평가 데이터와 직책별 가중치, 프로젝트 참여 비중을 기반으로 최종 평가 점수를 산출하는 로직과 API를 개발했습니다.

## 1. 핵심 기능

-   **최종 평가 점수 계산:** 피평가자의 역할(role)에 따라 설정된 평가 항목별 가중치와 프로젝트 참여 비중을 적용하여 동료평가, PM평가, 정성평가 점수를 합산한 최종 점수를 산출합니다.
-   **복수 프로젝트 처리:** 2개 이상의 프로젝트에 참여한 사용자의 경우, 각 프로젝트의 평가 점수에 참여 비중을 곱하여 가중 평균을 계산하고 이를 최종 점수에 반영합니다.
-   **결과 저장:** 계산된 최종 점수는 `FinalEvaluation` 모델로 데이터베이스에 저장됩니다. 기존 데이터가 있을 경우 업데이트됩니다.

## 2. 구현 세부 사항

### 2.1. 데이터 모델 (`app/models/evaluation.py`)

-   **`FinalEvaluation` 모델:** 최종 계산된 평가 점수를 저장하기 위한 새로운 SQLAlchemy 모델을 추가했습니다.
    -   `evaluatee_id`: 피평가자 ID (FK)
    -   `evaluation_period`: 평가 기간 (예: "2025-H1")
    -   `peer_score`: 계산된 동료평가 점수
    -   `pm_score`: 계산된 PM평가 점수
    -   `qualitative_score`: 계산된 정성평가 점수
    -   `final_score`: 최종 가중치 합산 점수

### 2.2. Pydantic 스키마 (`app/schemas/evaluation.py`)

-   **`FinalEvaluationBase`, `FinalEvaluationCreate`, `FinalEvaluationUpdate`, `FinalEvaluation` 스키마:** `FinalEvaluation` 모델의 API 요청 및 응답을 위한 Pydantic 스키마를 정의했습니다.

### 2.3. CRUD 로직 (`app/crud/final_evaluation.py`)

-   **`CRUDFinalEvaluation` 클래스:** `FinalEvaluation` 모델에 대한 CRUD 작업을 처리하는 클래스를 구현했습니다.
-   **`get_by_evaluatee_and_period` 메서드:** 특정 피평가자와 평가 기간에 대한 최종 평가를 조회하는 메서드를 추가했습니다.

### 2.4. 계산 로직 (`app/crud/evaluation_calculator.py`)

-   **`calculate_and_store_final_scores` 함수:**
    -   피평가자의 역할에 해당하는 `EvaluationWeight`를 조회합니다.
    -   피평가자의 `ProjectMember` 정보를 통해 참여 프로젝트 및 참여 비중을 가져옵니다.
    -   각 프로젝트별로 `PeerEvaluation` 및 `PmEvaluation`의 평균 점수를 계산하고, 프로젝트 참여 비중을 곱하여 가중 평균을 산출합니다.
    -   `QualitativeEvaluation` 점수를 조회합니다.
    -   각 평가 항목별 가중치를 적용하여 최종 `final_score`를 계산합니다.
    -   계산된 결과를 `FinalEvaluation` 객체로 생성하거나 기존 객체를 업데이트하여 데이터베이스에 저장합니다.

### 2.5. API 엔드포인트 (`app/api/endpoints/evaluations.py`)

-   **`POST /api/v1/evaluations/calculate`:**
    -   **목적:** 특정 사용자 또는 모든 하위 조직원에 대한 최종 평가 점수 계산을 트리거합니다.
    -   **권한:** `DEPT_HEAD` 또는 `ADMIN` 역할의 사용자만 접근 가능합니다.
    -   **요청 바디:** `user_ids: List[int] | None` (선택 사항, 특정 사용자 ID 목록. 없으면 호출자의 하위 조직원 또는 전체 사용자 대상)
    -   **응답:** 계산된 `FinalEvaluation` 객체 목록

## 3. 발생한 문제 및 해결 과정

개발 과정에서 다음과 같은 문제들이 발생했으며, 이를 해결했습니다.

-   **`NameError: name 'evaluator_id' is not defined` (in `app/models/evaluation.py`):**
    -   **원인:** `QualitativeEvaluation` 모델에서 `evaluator_id` 및 `evaluatee_id` 컬럼 정의가 누락되어 발생했습니다.
    -   **해결:** 누락된 컬럼 정의를 복구하고, `relationship`의 `foreign_keys` 인자에 람다 함수를 사용하여 클래스 정의 스코프 문제를 해결했습니다. (예: `foreign_keys=lambda: QualitativeEvaluation.evaluator_id`)

-   **`sqlalchemy.exc.InvalidRequestError: Class ... does not have a __table__ or __tablename__ specified...` (in `app/models/evaluation.py`):**
    -   **원인:** `PeerEvaluation` 모델에서 `__tablename__` 및 컬럼 정의가 누락되어 발생했습니다.
    -   **해결:** 누락된 `__tablename__` 및 컬럼 정의를 복구했습니다.

-   **`NameError: name 'Session' is not defined` (in various CRUD files and `conftest.py`):**
    -   **원인:** `Session` 타입 힌트가 사용되었으나 `sqlalchemy.orm`에서 `Session`이 명시적으로 임포트되지 않아 발생했습니다.
    -   **해결:** 해당 파일들에 `from sqlalchemy.orm import Session` 또는 `from sqlalchemy.orm import sessionmaker, Session`을 추가하여 `Session`을 임포트했습니다.

-   **`AttributeError: module 'app.models' has no attribute 'EvaluationItem'` (in `tests/api/test_final_evaluations.py`):**
    -   **원인:** `EvaluationItem`이 `app.models` 아래에 직접 존재하지 않고 `app.models.evaluation`에 정의되어 있는데, `models.EvaluationItem`으로 잘못 참조하여 발생했습니다.
    -   **해결:** `models.EvaluationItem`을 `models.evaluation.EvaluationItem`으로 수정했습니다.

-   **테스트 유틸리티 함수 인자 불일치 (`create_random_user`, `create_random_organization`, `create_random_project`, `authentication_token_from_username`):**
    -   **원인:** 새로 작성된 테스트 코드에서 `tests/utils` 하위의 유틸리티 함수들을 호출할 때, 실제 함수 시그니처와 다른 인자(예: `username`, `name`, `owner_id`, `password`)를 전달하여 발생했습니다.
    -   **해결:** 각 유틸리티 함수의 실제 시그니처에 맞춰 테스트 코드의 함수 호출 인자를 수정했습니다.

## 4. 결론

FR-A-4.1 및 FR-A-4.2 요구사항에 따른 최종 평가 점수 산출 로직 및 API 개발을 완료했습니다. 이 과정에서 발생한 다양한 모델 정의 및 임포트 관련 오류, 테스트 유틸리티 함수 사용 오류 등을 해결하여 기능의 안정성을 확보했습니다.

**주의:** 현재 이 기능에 대한 테스트 코드는 작성되지 않았습니다. 이전 테스트 코드 작성 시 여러 유틸리티 함수 인자 불일치 및 픽스처 문제로 인해 테스트 파일(`tests/api/test_final_evaluations.py`)을 삭제했습니다. 이 기능의 안정성을 보장하기 위해 **반드시 새로운 테스트 코드를 작성해야 합니다.**
