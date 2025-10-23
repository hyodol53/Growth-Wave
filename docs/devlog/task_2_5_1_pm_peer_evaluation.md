# Task 2.4: PM동료평가 API 개발 (FR-A-3.1)

`REQUIREMENTS.md`의 FR-A-3.1 요구사항에 따라, 피평가자는 자신을 제외한 프로젝트 동료에게 점수를 부여한다. 부여하는 점수의 평균은 70점을 초과할 수 없으며, 초과 시 시스템은 제출을 제한하고 사용자에게 알림을 표시해야 한다는 요구사항을 구현했습니다.

-   **데이터 모델:** `app/models/evaluation.py`에 `PeerEvaluation` 모델을 새로 추가하여 동료평가 데이터를 저장합니다.
-   **Pydantic 스키마:** `app/schemas/evaluation.py`에 `PeerEvaluationBase`, `PeerEvaluationCreate`, `PeerEvaluationInDBBase`, `PeerEvaluation` 스키마를 추가하여 API 요청 및 응답을 처리합니다.
-   **CRUD 작업:** `app/crud/peer_evaluation.py`에 `CRUDPeerEvaluation` 클래스와 `create_multi` 메서드를 구현하여 다수의 동료 평가를 일괄적으로 생성합니다.
-   **API 엔드포인트:** `app/api/endpoints/evaluations.py`에 `POST /api/v1/evaluations/peer-evaluations/` 엔드포인트를 추가하여 동료 평가 제출 기능을 제공합니다. 이 엔드포인트는 제출된 평가 점수의 평균이 70점을 초과하지 않도록 유효성을 검사합니다.
-   **테스트:** `tests/api/test_peer_evaluations.py` 파일을 생성하고 다음 시나리오에 대한 테스트 케이스를 구현하여 기능의 정확성과 안정성을 검증했습니다.
    - 동료 평가 성공적으로 생성
    - 평균 점수가 70점을 초과하는 경우 평가 생성 실패
    - 인증되지 않은 사용자의 평가 생성 시도 실패

**해결된 문제점:**
-   `app/schemas/__init__.py`: `PeerEvaluation` 스키마 임포트 누락으로 인한 `AttributeError` 해결.
-   `app/api/endpoints/evaluations.py`: `deps.get_current_active_user` 대신 `deps.get_current_user` 사용으로 수정.
-   `app/api/endpoints/evaluations.py`: `typing.Any` 임포트 누락으로 인한 `NameError` 해결.
-   `tests/api/test_peer_evaluations.py`, `tests/utils/project.py`: `app.tests.utils` 참조 대신 `tests.utils` 사용으로 임포트 경로 수정.
-   `tests/utils/project.py`: `ProjectCreate` 스키마의 `owner_org_id` 필드가 누락되어 발생한 `ValidationError` 해결을 위해 `create_random_organization` 유틸리티 함수 추가 및 `owner_org_id` 전달.
-   `tests/utils/organization.py`: `crud.organization.organization.create` 대신 `crud.organization.create_organization` 직접 호출하도록 수정.
-   `app/crud/__init__.py`: `project` CRUD 모듈 임포트 누락으로 인한 `AttributeError` 해결.
-   `app/models/__init__.py`: `Project` 및 `ProjectMember` 모델 임포트 누락으로 인한 `AttributeError` 해결.
-   `tests/utils/project_member.py`: `ProjectMemberCreate` 스키마에서 `weight` 대신 `participation_weight` 사용하도록 수정.
-   `app/core/config.py`: `API_V1_STR` 설정값 누락으로 인한 `AttributeError` 해결.
-   `tests/api/test_peer_evaluations.py`, `tests/utils/user.py`: `create_random_user` 함수에 `password` 인자 추가 및 테스트에서 `user1.email` 대신 `user1.username`을 인증에 사용하도록 수정하여 `KeyError: 'access_token'` 문제 해결.

**결론:** 식별된 모든 테스트 실패가 해결되었으며, 전체 테스트 스위트가 이제 통과하여 'PM동료평가 API' 기능의 안정적인 구현을 확인했습니다.