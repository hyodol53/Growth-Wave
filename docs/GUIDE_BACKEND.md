# 백엔드 개발 가이드라인

이 문서는 백엔드 개발 에이전트가 준수해야 할 환경 설정, 규칙, 체크리스트 등을 정의합니다.

## 1. 개발 환경 설정

### 1.1. 사전 요구사항

*   Python 3.10
*   Poetry

### 1.2. 설치

1.  **Clone the repository.**
2.  **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```

### 1.3. 애플리케이션 실행

*   FastAPI 애플리케이션을 개발 모드(auto-reload)로 실행합니다:
    ```bash
    poetry run uvicorn app.main:app --reload
    ```

### 1.4. 테스트 실행

*   전체 테스트를 실행합니다:
    ```bash
    poetry run pytest
    ```

## 2. 개발 규칙 및 체크리스트

### 2.1. 테스트 코드 작성 (Writing Test Code)

*   **테스트 코드 필수 작성**: 모든 백엔드 기능 개발, 수정, 버그 픽스 시에는 반드시 해당 변경 사항을 검증하는 테스트 코드를 작성해야 합니다.
*   **테스트 위치**: 테스트 코드는 `tests/` 디렉토리 하위에 관련 도메인에 맞춰 작성합니다. (예: `tests/api/test_users.py`)
*   **실행**: 새로운 코드가 추가되거나 변경될 때마다 `poetry run pytest`를 실행하여 전체 테스트가 통과하는지 확인해야 합니다.

### 2.2. API 문서 작성 (API Documentation)

*   **API 문서화 필수**: 새로운 API를 추가하거나 기존 API를 수정하는 경우, 반드시 해당 변경 사항을 문서화해야 합니다.
*   **문서 위치**: API 문서는 `docs/api/` 디렉터리 하위에 작성합니다.
*   **구조**: 기능 도메인별로 하위 디렉터리를 생성하고 (예: `docs/api/users/`), 각 엔드포인트에 대한 문서는 별도의 Markdown 파일로 작성합니다.
*   **필수 포함 내용**: 각 API 문서에는 다음 내용이 반드시 포함되어야 합니다.
    *   HTTP 메서드 및 전체 URL (예: `POST /api/v1/users/`)
    *   API에 대한 명확한 설명
    *   필요한 경우, 접근에 필요한 권한 (예: 관리자, 실장 등)
    *   요청(Request) 형식, 헤더, 본문 예시
    *   성공 시 응답(Response) 형식, 상태 코드, 본문 예시
    *   발생 가능한 주요 오류 및 상태 코드

### 2.3. 신규 기능 추가 시 체크리스트 (Checklist for Adding New Features)

잦은 시행착오를 방지하고 일관성 있는 개발을 위해, 새로운 기능을 추가할 때 다음 사항을 반드시 확인합니다.

*   **`__init__.py` 파일 업데이트 확인**
    *   새로운 `schemas` 또는 `crud` 모듈(예: `app/schemas/new_feature.py`)을 추가했나요?
    *   그렇다면, 해당 패키지의 `__init__.py` 파일(예: `app/schemas/__init__.py`)에 새로운 클래스나 객체를 import하여 패키지 레벨에서 `app.schemas.NewFeature`와 같이 접근할 수 있도록 했는지 확인하세요. 이 과정을 누락하면 `AttributeError`가 발생합니다.

*   **API/CRUD 호출 규약 확인**
    *   API 엔드포인트에서 CRUD 함수를 호출할 때, 기존 코드의 호출 방식을 확인하고 일관성을 유지하세요.
    *   예를 들어, `crud.user.user.get()`과 같이 `crud.<모듈명>.<인스턴스명>.<메서드>()` 패턴을 따르는지 확인해야 합니다. `crud.<인스턴스명>`으로 잘못 호출하면 `AttributeError`가 발생합니다.

*   **의존성 및 유틸리티 함수 확인**
    *   테스트 코드나 API에서 필요한 의존성 주입 함수(예: `deps.get_current_admin_user`)나 유틸리티 함수(예: `random_lower_string`)를 사용하기 전에, 해당 함수가 어느 파일에 정의되어 있는지, 정확한 이름은 무엇인지 먼저 확인하세요. 다른 파일의 사용 예시를 참고하는 것이 가장 좋습니다.

*   **테스트 Fixture 및 패턴 확인**
    *   테스트 작성 시, `pytest` fixture(예: `superuser_token_headers`)를 가정하고 사용하기 전에 `tests/conftest.py` 파일을 먼저 확인하세요.
    *   인증 헤더의 경우, 각 테스트 함수 내에서 `create_random_user`와 `authentication_token_from_username` 유틸리티를 호출하여 직접 생성하는 것이 이 프로젝트의 기본 패턴입니다. 기존 테스트 파일의 구현 방식을 반드시 먼저 확인하고 따르세요.

### 2.4. 데이터베이스 스키마 변경 (Database Schema Changes)

*   **마이그레이션 스크립트 작성**: `app/models/` 디렉터리의 SQLAlchemy 모델을 수정하여 데이터베이스 스키마에 변경이 발생하는 경우, 반드시 `migrations/` 디렉터리에 순수 SQL로 작성된 마이그레이션 스크립트를 추가해야 합니다.

*   **파일명 규칙**: 스크립트 파일명은 `XXX_description.sql` 형식을 따릅니다. (예: `001_add_evaluation_comments.sql`, `002_create_new_table.sql`)

*   **작성 가이드**:
    *   스크립트에는 변경 사항을 적용하기 위한 `ALTER TABLE`, `CREATE TABLE` 등의 SQL 구문을 포함해야 합니다.
    *   데이터 무결성을 보장하기 위해 모든 변경 사항은 하나의 트랜잭션(`BEGIN TRANSACTION;` ... `COMMIT;`) 내에서 실행하는 것을 권장합니다.
    *   각 SQL 구문의 목적을 설명하는 주석을 추가하여 다른 개발자가 변경 내역을 쉽게 이해할 수 있도록 합니다.
    *   (참고: `migrations/001_add_evaluation_comments.sql`)
