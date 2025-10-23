# Task 2.3: 평가 항목 가중치 설정 기능 개발

`REQUIREMENTS.md`의 **FR-A-2.3** 요구사항에 따라, 시스템 관리자가 직책별 평가 항목의 가중치(%)를 설정할 수 있는 기능의 백엔드 개발을 완료했습니다.

- **핵심 기능**: 관리자는 향후 평가 점수 산출(FR-A-4.1)에 사용될 각 평가 항목(동료평가, PM평가, 정성평가 등)의 가중치를 직책(`employee`, `team_lead` 등)별로 생성, 조회, 수정, 삭제할 수 있습니다.

- **데이터베이스 모델 (`app/models/evaluation.py`)**:
    - `EvaluationWeight` 모델을 새로 추가하여 직책, 평가 항목, 가중치 값을 저장합니다.
    - 평가 항목(`EvaluationItem`)과 사용자 역할(`UserRole`)은 `Enum`으로 관리하여 데이터의 일관성을 보장합니다.

- **API 엔드포인트 (`app/api/endpoints/evaluations.py`)**:
    - `/api/v1/evaluations/` 경로에 CRUD 엔드포인트를 구현했습니다.
    - `get_current_admin_user` 의존성을 사용하여 모든 엔드포인트는 **관리자(admin) 권한**을 가진 사용자만 접근할 수 있도록 보호됩니다.

- **테스트 및 안정화 (`tests/api/test_evaluations.py`)**:
    - 기능의 정상 동작(CRUD)과 더불어, 일반 사용자가 해당 API에 접근 시 403 Forbidden 오류를 반환하는지 확인하는 권한 테스트 케이스를 포함하여 기능의 안정성과 보안을 검증했습니다.
    - 개발 과정에서 `AttributeError`, `ModuleNotFoundError`, `fixture not found` 등 다양한 유형의 오류를 마주쳤습니다. `__init__.py` 파일 수정, 잘못된 함수명 및 모듈 경로 수정, 테스트 코드 리팩토링 등 반복적인 디버깅을 통해 모든 문제를 해결하고 전체 테스트 스위트(31개) 통과를 확인했습니다.