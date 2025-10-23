# Task 2.6.1: 최종 등급 산출 로직 테스트 개발 및 안정화

`REQUIREMENTS.md`의 FR-A-4.1 및 FR-A-4.2 요구사항에 따라 구현된 최종 등급 산출 로직(`app/crud/evaluation_calculator.py`)과 API 엔드포인트(`POST /api/v1/evaluations/calculate`)의 정확성과 안정성을 검증하기 위한 테스트 코드를 개발하고 안정화했습니다.

## 1. 테스트 목표

-   다양한 사용자 역할(DEPT_HEAD, EMPLOYEE)에 따른 API 접근 권한 검증.
-   프로젝트 참여 비중 및 직책별 평가 항목 가중치를 반영한 최종 점수 계산 로직의 정확성 검증.
-   기존 최종 평가 기록이 있을 경우 업데이트, 없을 경우 새로 생성되는지 확인.

## 2. 구현 세부 사항

-   **테스트 파일:** `tests/api/test_final_evaluations.py`를 새로 생성했습니다.
-   **테스트 케이스:**
    -   `test_calculate_final_evaluations_as_dept_head`: DEPT_HEAD 권한을 가진 사용자가 최종 평가를 성공적으로 계산하고 저장하는 시나리오를 테스트합니다. 여러 프로젝트에 참여한 직원의 점수 합산 및 가중치 적용 로직을 검증합니다.
    -   `test_calculate_final_evaluations_unauthorized`: EMPLOYEE 권한을 가진 사용자가 최종 평가 계산을 시도할 때 403 Forbidden 오류가 발생하는지 검증합니다.
-   **테스트 유틸리티 함수 개선:**
    -   `tests/utils/project_member.py`의 `create_random_project_member` 함수 이름이 `create_project_member`로 수정되었습니다.
    -   `tests/utils/evaluation.py` 파일이 새로 생성되었으며, `create_random_evaluation_weight`, `create_random_peer_evaluation`, `create_random_pm_evaluation`, `create_random_qualitative_evaluation` 함수가 포함되어 테스트 데이터 생성을 용이하게 했습니다.
    -   `create_random_*_evaluation` 함수들이 `PeerEvaluationCreate`, `PmEvaluationCreate`, `QualitativeEvaluationCreate` 스키마의 `evaluations: List[BaseModel]` 구조에 맞게 데이터를 구성하도록 수정되었습니다.
    -   테스트 시점의 `evaluation_period`를 동적으로 생성하여 모든 평가 생성 유틸리티 함수에 일관되게 전달하도록 수정했습니다.

## 3. 발생한 문제 및 해결 과정

테스트 개발 및 안정화 과정에서 다음과 같은 문제들이 발생했으며, 이를 해결했습니다.

-   **`ImportError: cannot import name 'create_random_project_member'`:**
    -   **원인:** `tests/api/test_final_evaluations.py`에서 `tests/utils/project_member.py`의 `create_random_project_member` 함수를 잘못된 이름으로 임포트하여 발생했습니다.
    -   **해결:** `create_random_project_member`를 올바른 함수명인 `create_project_member`로 수정했습니다.

-   **`ModuleNotFoundError: No module named 'tests.utils.evaluation'`:**
    -   **원인:** `tests/utils/evaluation.py` 파일이 존재하지 않아 발생했습니다.
    -   **해결:** `create_random_evaluation_weight`, `create_random_peer_evaluation`, `create_random_pm_evaluation`, `create_random_qualitative_evaluation` 유틸리티 함수를 포함하는 `tests/utils/evaluation.py` 파일을 새로 생성했습니다.

-   **`AttributeError: PEER` (in `tests/utils/evaluation.py`):**
    -   **원인:** `EvaluationItem.PEER`와 같이 `EvaluationItem` Enum의 멤버 이름을 잘못 참조하여 발생했습니다. 올바른 이름은 `PEER_REVIEW`, `PM_REVIEW`, `QUALITATIVE_REVIEW`였습니다.
    -   **해결:** `tests/utils/evaluation.py` 및 `tests/api/test_final_evaluations.py`에서 `EvaluationItem` 멤버 이름을 올바르게 수정했습니다.

-   **`TypeError: create_random_project() got an unexpected keyword argument 'owner_id'`:**
    -   **원인:** `create_random_project` 함수가 `owner_id` 인자를 받지 않는데, `tests/api/test_final_evaluations.py`에서 이를 전달하여 발생했습니다. 프로젝트는 조직에 의해 소유됩니다.
    -   **해결:** `tests/api/test_final_evaluations.py`에서 `create_random_project` 호출 시 `owner_id` 인자를 제거했습니다.

-   **`pydantic_core._pydantic_core.ValidationError: 1 validation error for PeerEvaluationCreate`:**
    -   **원인:** `PeerEvaluationCreate`, `PmEvaluationCreate`, `QualitativeEvaluationCreate` 스키마가 `evaluations: List[BaseModel]` 형태의 요청 본문을 예상하는데, 유틸리티 함수에서 개별 필드를 직접 전달하여 발생했습니다.
    -   **해결:** `tests/utils/evaluation.py`의 유틸리티 함수들을 수정하여 `BaseModel` 객체를 리스트로 래핑하여 `Create` 스키마에 전달하도록 했습니다.

-   **`AssertionError: assert 422 == 403` (for unauthorized test):**
    -   **원인:** `POST /api/v1/evaluations/calculate` 엔드포인트의 `user_ids` 파라미터가 Pydantic 모델로 래핑되지 않아 FastAPI가 JSON 본문을 올바르게 파싱하지 못하고 `422 Unprocessable Entity`를 반환했습니다.
    -   **해결:** `app/schemas/evaluation.py`에 `FinalEvaluationCalculateRequest` 스키마를 정의하고, `app/api/endpoints/evaluations.py`의 엔드포인트에서 이를 요청 본문으로 받도록 수정했습니다. 또한 테스트 코드에서도 이 스키마를 사용하여 요청을 보내도록 변경했습니다.

-   **`SyntaxError: invalid syntax` (in `app/api/endpoints/evaluations.py`):**
    -   **원인:** `user_ids = request_body.user_ids`와 `if current_user.role not in [...]` 문이 한 줄에 잘못 연결되어 발생했습니다.
    -   **해결:** 두 문장을 별도의 줄로 분리하여 `SyntaxError`를 해결했습니다.

-   **`AttributeError: module 'app.schemas' has no attribute 'FinalEvaluationCalculateRequest'`:**
    -   **원인:** `app/api/endpoints/evaluations.py`에서 `FinalEvaluationCalculateRequest` 스키마를 임포트하지 않아 발생했습니다.
    -   **해결:** `app/api/endpoints/evaluations.py`에 `from app.schemas.evaluation import FinalEvaluationCalculateRequest` 임포트 문을 추가했습니다.

-   **`AttributeError: 'CRUDFinalEvaluation' object has no attribute 'final_evaluation'`:**
    -   **원인:** `app/crud/evaluation_calculator.py`에서 `crud.final_evaluation.final_evaluation.get_by_evaluatee_and_period`와 같이 `CRUDFinalEvaluation` 인스턴스를 잘못 참조하여 발생했습니다. 올바른 참조는 `crud.final_evaluation.get_by_evaluatee_and_period`입니다.
    -   **해결:** `crud.final_evaluation` 인스턴스에 대한 중복 참조를 제거했습니다.

-   **`AssertionError: assert 0.0 == 76.0` (for `peer_score`):**
    -   **원인:** `app/crud/evaluation_calculator.py`에서 `evaluation_period`가 동적으로 생성되는데, 테스트 유틸리티 함수에서 `evaluation_period`를 하드코딩하여 데이터 불일치가 발생했습니다.
    -   **해결:** `tests/api/test_final_evaluations.py`에서 `test_evaluation_period`를 동적으로 생성하고, 모든 평가 생성 유틸리티 함수에 이를 전달하도록 수정했습니다. 또한 `tests/utils/evaluation.py`의 유틸리티 함수들도 `evaluation_period` 인자를 받도록 수정했습니다.

-   **`AssertionError: assert 8580.0 == 85.8` (for `final_score`):**
    -   **원인:** `app/crud/evaluation_calculator.py`에서 평가 항목 가중치(예: 30.0, 50.0, 20.0)를 백분율로 사용하면서 100으로 나누지 않고 계산하여 발생했습니다.
    -   **해결:** `app/crud/evaluation_calculator.py`의 최종 점수 계산 로직에서 `weight_map`에서 가져온 가중치를 100.0으로 나누어 적용하도록 수정했습니다.

## 4. 결론

위의 모든 문제 해결을 통해 `poetry run pytest` 실행 시 모든 테스트(43개)가 성공적으로 통과하는 것을 확인했습니다. 이로써 최종 등급 산출 로직의 기능적 정확성과 안정성이 확보되었습니다.