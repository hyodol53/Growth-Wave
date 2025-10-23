# Task 2.6: 정성평가 API 개발 (FR-A-3.5)

`REQUIREMENTS.md`의 FR-A-3.5 요구사항('팀장/실장은 피평가자에게 100점 만점의 정성평가 점수를 부여한다')에 따라, 팀장 및 실장이 자신의 하위 조직원에게 정성평가 점수를 부여할 수 있는 API를 개발했습니다.

- **데이터 모델 (`app/models/evaluation.py`)**:
    - `QualitativeEvaluation` 모델을 새로 추가하여 정성평가 데이터를 저장합니다. 이 모델은 평가자(팀장/실장), 피평가자, 점수 등의 정보를 포함합니다.

- **API 스키마 (`app/schemas/evaluation.py`)**:
    - `QualitativeEvaluationCreate`, `QualitativeEvaluation` 등 정성평가 API의 요청 및 응답에 사용될 Pydantic 스키마를 정의했습니다.

- **CRUD 로직 (`app/crud/qualitative_evaluation.py`)**:
    - `CRUDQualitativeEvaluation` 클래스를 생성하고, 여러 평가를 일괄적으로 데이터베이스에 생성하는 `create_multi` 메서드를 구현했습니다.

- **API 엔드포인트 (`app/api/endpoints/evaluations.py`)**:
    - `POST /api/v1/evaluations/qualitative-evaluations/` 엔드포인트를 구현했습니다.
    - **권한 제어**: 요청을 보낸 사용자가 `TEAM_LEAD` 또는 `DEPT_HEAD` 역할인지, 그리고 피평가자가 자신의 하위 조직에 속해 있는지 확인하는 검증 로직을 추가하여, 오직 상급자만이 자신의 하위 조직원에게 평가를 제출할 수 있도록 제한했습니다.
    - **유효성 검사**: 점수가 0점에서 100점 사이인지 확인하는 로직을 추가했습니다.

- **테스트 및 안정화 (`tests/api/test_qualitative_evaluations.py`)**:
    - 기능의 정상 동작(성공적인 평가 제출)을 검증하는 테스트 케이스를 작성했습니다.
    - 비정상 케이스(권한 없는 사용자의 제출 시도, 자신의 하위 조직원이 아닌 사용자에 대한 제출 시도, 점수 범위를 벗어난 제출)에 대한 권한 및 유효성 검사 로직이 올바르게 동작하는지(각각 403, 403, 400 오류 반환) 확인했습니다.
    - 테스트 실행 중 `IndentationError`, `ImportError`, `AttributeError` 등 다양한 오류를 마주쳤습니다. 잘못된 들여쓰기 수정, `authentication_token_from_username` 유틸리티 함수의 정확한 경로 파악 및 수정, `UserRole` Enum 값의 대소문자 오류 수정 등을 통해 모든 문제를 해결하고, 전체 테스트 스위트(41개)가 모두 통과하는 것을 확인하여 기능의 안정성을 확보했습니다.

**결론:**
정성평가 기능의 백엔드 구현이 안정적으로 완료되었으며, 엄격한 권한 제어와 유효성 검사를 통해 요구사항을 충족했음을 확인했습니다.
