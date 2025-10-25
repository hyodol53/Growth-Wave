# Task 4.1: 개별 조직 및 인원 관리 기능 개발

`REQUIREMENTS.md`의 `FR-A-1.4`, `FR-A-1.5`, `FR-A-1.6` 요구사항에 따라, 관리자가 개별 조직과 사용자를 UI를 통해 직접 생성, 수정, 삭제할 수 있는 백엔드 기능을 개발했습니다. 이는 기존의 파일 일괄 동기화 방식에 더해 세밀한 관리 기능을 제공합니다.

## 1. 개별 조직 관리 (FR-A-1.4)

- **API 스키마 (`app/schemas/organization.py`):**
    - 조직 정보 수정을 위해 `name`, `level`, `parent_id` 등 모든 필드가 선택적인 `OrganizationUpdate` Pydantic 스키마를 추가했습니다.

- **CRUD 로직 (`app/crud/organization.py`):**
    - `update_organization`: SQLAlchemy 모델 객체와 `OrganizationUpdate` 스키마를 받아 변경된 필드만 선택적으로 업데이트하는 함수를 구현했습니다.
    - `delete_organization`: 조직 ID를 받아 해당 조직을 데이터베이스에서 삭제하는 함수를 구현했습니다.

- **API 엔드포인트 (`app/api/endpoints/organizations.py`):**
    - `PUT /api/v1/organizations/{org_id}`: 특정 조직의 정보를 수정합니다.
    - `DELETE /api/v1/organizations/{org_id}`: 특정 조직을 삭제합니다.
    - 두 엔드포인트 모두 `get_current_admin_user` 의존성을 사용하여 관리자만 접근할 수 있도록 보호됩니다.

## 2. 개별 인원 관리 (FR-A-1.5, FR-A-1.6)

- **CRUD 로직 (`app/crud/user.py`):**
    - `CRUDUser` 클래스에 커스텀 `update` 메소드를 구현했습니다. 이 메소드는 `UserUpdate` 스키마를 입력받으며, 만약 `password` 필드가 포함된 경우 이를 안전하게 해싱하여 `hashed_password`로 변환한 후 데이터베이스에 업데이트합니다.

- **API 엔드포인트 (`app/api/endpoints/users.py`):**
    - `PUT /api/v1/users/{user_id}`: 특정 사용자의 정보(이름, 이메일, 역할, 소속 조직 등)를 수정합니다.
    - `DELETE /api/v1/users/{user_id}`: 특정 사용자를 시스템에서 삭제합니다.
    - 두 엔드포인트 모두 관리자 전용으로 구현되었습니다.

## 3. 테스트 및 안정화

- **테스트 코드 (`tests/api/test_organizations.py`, `tests/api/test_users.py`):**
    - 신규 API 엔드포인트의 정상 동작(CRUD)을 검증하는 테스트 케이스를 추가했습니다.
    - 관리자가 아닌 일반 사용자가 접근 시 403 Forbidden 오류를 반환하는지, 존재하지 않는 ID에 접근 시 404 Not Found 오류를 반환하는지 등 예외 케이스에 대한 테스트를 포함하여 기능의 안정성과 보안을 강화했습니다.

## 4. 코드 품질 개선 (Warning 수정)

- 개발 과정에서 `pytest` 실행 시 다수의 Pydantic V1 관련 경고가 발생하는 것을 확인했습니다.
- `app/schemas/` 디렉터리 내의 모든 Pydantic 모델의 `Config` 클래스를 Pydantic V2에서 권장하는 `model_config = ConfigDict(from_attributes=True)` 방식으로 수정했습니다.
- `praise.py` 스키마의 `min_items`/`max_items`를 `min_length`/`max_length`로 변경하고, `organization.py`의 `update_forward_refs()`를 `model_rebuild()`로 변경하는 등 V2 표준에 맞게 코드를 현대화했습니다.
- `app/crud/` 내에서 사용되던 `.dict()` 메소드를 `.model_dump()`로 변경했습니다.
- 이 리팩토링 작업을 별도의 커밋으로 분리하여 코드베이스의 품질을 개선했습니다.
