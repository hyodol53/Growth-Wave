# Task 2.2: 프로젝트 참여 비중 설정 API 개발 (FR-A-1.3)

`REQUIREMENTS.md`의 FR-A-1.3 요구사항에 따라, 실장이 평가 기간 내 소속 인원의 프로젝트별 참여 비중(%)을 설정할 수 있어야 하며, 총합은 100%여야 한다는 요구사항을 구현했습니다.

-   **데이터 모델:** 새로운 SQLAlchemy 모델인 `Project`와 `ProjectMember`를 도입하고, 관계 설정을 위해 기존 모델을 업데이트했습니다.
-   **Pydantic 스키마:** API 상호작용을 위한 데이터 유효성 검사 및 직렬화를 처리하기 위해 `Project` 및 `ProjectMember`에 해당하는 Pydantic 스키마를 생성했습니다.
-   **CRUD 작업:** `Project` 및 `ProjectMember`를 위한 전용 CRUD 모듈(예: `CRUDBase`)을 개발하고, 새로운 관계를 수용하기 위해 `user` CRUD 로직을 리팩토링했습니다.
-   **API 엔드포인트:** `POST /api/v1/projects/members/weights` 엔드포인트를 생성했으며, 100% 합계 제약 조건을 강제하기 위한 강력한 권한 부여 및 유효성 검사 로직을 포함했습니다.
-   **테스트:** `tests/api/test_projects.py`에 관련 테스트 케이스를 개발하여 프로젝트 참여 비중 설정 API의 올바른 기능과 제약 조건을 검증했습니다.

**해결된 문제점:**
-   **`TypeError` 해결:**
    *   **원인:** 테스트 유틸리티 함수 `authentication_token_from_username`이 키워드 전용 인자를 받도록 정의되었으나, `tests/api/test_projects.py`에서 위치 인자로 잘못 호출되었습니다.
    *   **해결:** 이 함수에 대한 모든 호출을 키워드 인자(예: `client=client, username=...`)를 사용하도록 수정했습니다.
-   **`AttributeError` 해결:**
    *   **원인:** `projects` API 엔드포인트에서 `project_member` CRUD 모듈을 잘못 호출했습니다. 코드가 임포트된 모듈(`crud_pm.get_multi_by_user`)에서 직접 메서드를 호출하려고 시도했습니다.
    *   **해결:** `crud_user` 모듈 사용법과 일관되게 실제 인스턴스를 통해 메서드를 호출하도록 수정했습니다(예: `crud_pm.project_member.get_multi_by_user` 및 `crud_pm.project_member.create`).
-   **`AssertionError` 해결:**
    *   **원인:** 권한 없는 API 접근 테스트(`test_set_project_member_weights_unauthorized_role`)가 실패했는데, 이는 예상 오류 메시지(`"not enough privileges"`)가 API의 실제 응답(`"The user doesn't have enough privileges for this operation"`)과 정확히 일치하지 않았기 때문입니다.
    *   **해결:** 테스트의 `assert` 문을 실제 오류 메시지의 부분 일치(`"doesn't have enough privileges"`)를 확인하도록 업데이트했습니다.

**결론:** 식별된 모든 테스트 실패가 해결되었으며, 전체 테스트 스위트가 이제 통과하여 '프로젝트 참여 비중 설정' 기능의 안정적인 구현을 확인했습니다.