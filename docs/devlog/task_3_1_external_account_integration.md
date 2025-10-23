# Task 3.1: 외부 계정 연동 기능 개발

`WORK_PLAN.md`의 **Task 3.1**에 해당하는 외부 계정 연동 기능의 백엔드 개발을 완료했습니다. 사용자는 이 기능을 통해 자신의 Jira, GitHub, Bitbucket 계정을 시스템에 안전하게 등록하고 관리할 수 있습니다.

- **보안 중심 설계**: 사용자가 제공하는 `access_token`은 `Fernet`을 사용하여 **암호화된 상태**로 `encrypted_access_token` 필드에 저장됩니다. 이를 통해 민감한 사용자 정보가 평문으로 데이터베이스에 노출되는 것을 방지합니다. 또한, API 응답 스키마(`schemas.ExternalAccount`)는 암호화된 토큰 값을 클라이언트에 다시 전송하지 않도록 설계되었습니다.

- **데이터베이스 모델 (`app/models/external_account.py`)**:
    - `ExternalAccount` 모델은 외부 계정 정보를 저장합니다.
    - `account_type`: 계정의 종류(`jira`, `github`, `bitbucket`)를 `Enum`으로 관리합니다.
    - `encrypted_access_token`: 암호화된 액세스 토큰을 저장합니다.
    - `owner_id`: 시스템의 내부 사용자와 외부 계정을 연결하는 `ForeignKey`입니다.

- **API 엔드포인트 (`app/api/endpoints/external_accounts.py`)**:
    - `/api/v1/external-accounts/` 경로에 다음 API를 구현했습니다.
        - `POST /`: 현재 로그인한 사용자의 외부 계정을 새로 등록합니다.
        - `GET /`: 현재 로그인한 사용자가 소유한 모든 외부 계정 목록을 조회합니다.
        - `DELETE /{account_id}`: 특정 외부 계정을 삭제합니다. 이때, 요청자가 계정의 소유자인지 확인하여 권한 없는 삭제를 방지합니다.

- **CRUD 로직 (`app/crud/external_account.py`)**:
    - 계정 생성 시 액세스 토큰을 암호화하는 로직을 포함합니다.
    - 사용자를 기준으로 계정을 조회하고, ID를 기준으로 삭제하는 데이터베이스 처리 함수들을 구현했습니다.

- **테스트 코드 (`tests/api/test_external_accounts.py`)**:
    - 계정 생성, 조회, 삭제의 기본 기능과 더불어, **다른 사용자의 계정을 삭제하려는 시도를 거부하는지**(`test_delete_other_user_account_fails`) 확인하는 테스트 케이스를 포함하여 기능의 안정성과 보안을 검증했습니다.