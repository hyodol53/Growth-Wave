# Task 2.3: 평가 주기 및 등급 비율 설정 API 개발

`REQUIREMENTS.md`의 `FR-A-2.1`, `FR-A-2.2` 요구사항에 따라, 관리자가 평가 주기와 부서별 등급 비율을 설정할 수 있는 API 개발을 시도했습니다.

## 1. 작업 진행 내역

- **데이터베이스 모델 추가 (`app/models/evaluation.py`)**: `EvaluationPeriod`와 `DepartmentGradeRatio` SQLAlchemy 모델을 정의했습니다.
- **Pydantic 스키마 추가 (`app/schemas/evaluation.py`)**: API 요청/응답을 위한 `EvaluationPeriod` 및 `DepartmentGradeRatio` 스키마를 정의했습니다.
- **CRUD 로직 구현 (`app/crud/`)**: 신규 모델에 대한 CRUD 로직을 `evaluation_period.py`와 `department_grade_ratio.py` 파일로 각각 생성하고, `__init__.py`에 등록했습니다.
- **API 엔드포인트 추가 (`app/api/endpoints/evaluations.py`)**: 평가 주기와 등급 비율을 생성, 조회, 수정, 삭제하는 API 엔드포인트를 구현했습니다. 모든 엔드포인트는 관리자(`admin`) 권한으로 보호됩니다.
- **테스트 코드 작성 (`tests/api/test_evaluations.py`)**: 상기 기능의 정상 동작 및 권한 제어를 검증하기 위한 `pytest` 테스트 케이스를 추가했습니다.

## 2. 발생 문제점 및 현황

테스트 코드 실행 결과, 새로 추가된 평가 주기 관리 API 관련 테스트에서 지속적으로 실패가 발생하고 있습니다.

- **오류 명**: `sqlalchemy.exc.StatementError: (builtins.TypeError) SQLite Date type only accepts Python date objects as input.`

- **오류 상세 원인**:
  - SQLAlchemy의 `Date` 타입 컬럼은 데이터베이스에 값을 저장할 때 파이썬의 `datetime.date` 객체 타입을 기대합니다.
  - 하지만 `fastapi.testclient.TestClient`를 사용하는 테스트 코드에서는 HTTP 요청을 위해 `json` 파라미터에 날짜를 ISO 8601 형식의 **문자열** (예: `"2025-01-01"`)로 전달합니다.
  - FastAPI의 Pydantic 모델이 이 문자열을 `datetime.date` 객체로 변환하여 CRUD 레이어로 전달해야 하지만, 이 과정이 올바르게 처리되지 않아 문자열 값이 그대로 데이터베이스 드라이버(SQLAlchemy)까지 전달되면서 타입 불일치 오류가 발생합니다.

- **시도된 해결책 및 추가 문제**:
  1. **`datetime.date` 객체 직접 전달**: 테스트 데이터에 `isoformat()`을 사용하지 않고 `datetime.date` 객체를 직접 넣어봤으나, `TestClient`의 기본 JSON 인코더가 `date` 객체를 직렬화(serialize)하지 못해 `TypeError: Object of type date is not JSON serializable` 오류가 발생했습니다.
  2. **커스텀 JSON 인코더 적용**: `TestClient`에 `date` 객체를 직렬화하는 커스텀 인코더를 적용하려 했으나, 현재 프로젝트의 `TestClient` 버전이 `json_encoder` 인자를 지원하지 않아 `TypeError`가 발생하며 실패했습니다.

## 3. 결론

현재 평가 주기 설정 API는 날짜 데이터 타입 처리 문제로 인해 테스트를 통과하지 못하고 있는 상태입니다. 이 문제를 해결하기 위해 FastAPI/Pydantic의 타입 변환 과정을 좀 더 면밀히 디버깅하거나, 테스트 환경에서의 데이터 전송 방식을 수정하는 작업이 필요합니다. 이 문제 해결을 우선 과제로 삼아 다음 작업을 진행해야 합니다.
