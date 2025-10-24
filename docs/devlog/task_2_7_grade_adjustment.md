# Task 2.7: 등급 조정 API 개발 (FR-A-4.4, FR-A-4.5)

`REQUIREMENTS.md`의 FR-A-4.4("B+/B- 등급 조정") 및 FR-A-4.5("동점자 처리") 요구사항에 따라, 실장 및 관리자가 최종 등급을 조정할 수 있는 API를 개발했습니다.

## 1. 핵심 기능

- **등급 조정 API:** `POST /api/v1/evaluations/adjust-grades` 엔드포인트를 통해 특정 사용자들의 최종 등급을 수동으로 조정합니다.
- **역할 기반 권한 제어:**
    - `DEPT_HEAD`는 소속 부서원의 등급만 조정할 수 있습니다.
    - `ADMIN`은 모든 사용자의 등급을 조정할 수 있습니다.
- **B+/B- 인원수 검증:** `DEPT_HEAD`가 등급 조정 시, 부서 내 B+와 B- 등급의 인원수가 동일해야 한다는 제약조건을 검증합니다.
- **TO(정원) 검증:** `DEPT_HEAD`가 등급 조정 시, 부서에 할당된 S, A 등급의 TO를 초과할 수 없다는 제약조건을 검증합니다.

## 2. 기술적 구현 세부 사항

- **데이터 모델 수정:**
    - `app/models/evaluation.py`의 `FinalEvaluation` 모델에 최종 등급을 저장하기 위한 `grade` 컬럼을 추가했습니다.
    - `app/models/organization.py`의 `Organization` 모델에 부서 자체의 등급(예: S, A, B)을 저장하기 위한 `department_grade` 컬럼을 추가했습니다.

- **API 스키마 추가 (`app/schemas/evaluation.py`):**
    - 등급 조정 요청을 위한 `GradeAdjustment` 및 `GradeAdjustmentRequest` 스키마를 새로 정의했습니다.

- **CRUD 로직 분리 및 구현:**
    - `app/crud/grade_adjustment.py` 모듈을 신설하여 등급 조정과 관련된 복잡한 비즈니스 로직(B+/B- 검증, TO 검증)을 `adjust_grades_for_department` 함수로 구현했습니다.
    - `app/crud/department_grade_ratio.py`에 `get_by_grade` 메서드를 추가하여 부서 등급에 따른 TO 비율을 효율적으로 조회할 수 있도록 했습니다.

- **API 엔드포인트 (`app/api/endpoints/evaluations.py`):**
    - 신규 `adjust-grades` 엔드포인트는 `grade_adjustment` CRUD 모듈의 함수를 호출하여 비즈니스 로직을 수행하고, `GradeAdjustmentError` 및 `GradeTOExceededError`와 같은 커스텀 예외를 처리하여 명확한 오류 메시지를 반환합니다.

- **테스트 (`tests/api/test_grade_adjustments.py`):**
    - 성공적인 등급 조정(실장, 관리자) 시나리오
    - B+/B- 인원 불일치 시 실패하는 시나리오
    - TO를 초과하여 등급을 부여하려 할 때 실패하는 시나리오
    - 권한 없는 사용자의 접근 시도 등 다양한 정상 및 예외 케이스에 대한 테스트 코드를 작성하여 기능의 안정성과 보안을 검증했습니다.

## 4. 결론

등급 조정 기능의 백엔드 구현이 안정적으로 완료되었으며, 요구사항에 명시된 모든 제약 조건(역할, B+/B- 밸런스, TO)을 충족함을 테스트를 통해 확인했습니다. 이로써 Phase 2의 2.7 항목 개발이 완료되었습니다.
