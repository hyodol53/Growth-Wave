# Phase 1: 초기 프로젝트 설정 및 사용자 인증

이 문서는 핵심 구조, 데이터베이스 모델, 인증 메커니즘, 기본 사용자/조직 관리 API를 포함한 FastAPI 프로젝트의 초기 설정을 상세히 설명합니다.

## 1. 프로젝트 초기 설정 (핵심 구조, 모델, 스키마)

*   **FastAPI 애플리케이션 구조:** API 엔드포인트(`api/`), 핵심 로직(`core/`), CRUD 작업(`crud/`), 데이터베이스 모델(`models/`), Pydantic 스키마(`schemas/`)를 위한 하위 모듈을 포함하는 FastAPI 애플리케이션(`app/`)의 기본 디렉터리 구조를 확립했습니다.
*   **데이터베이스 모델 (SQLAlchemy):** `app/models/`에 핵심 데이터베이스 모델을 정의했습니다. 특히 사용자 정보를 위한 `user.py`와 조직 구조를 위한 `organization.py`를 포함합니다.
*   **Pydantic 스키마:** API 요청 및 응답을 위한 데이터 유효성 검사 및 직렬화를 위해 `app/schemas/`에 Pydantic 스키마를 구현했습니다. 여기에는 `user.py`, `organization.py`, `token.py`가 포함됩니다.
*   **메인 애플리케이션 진입점:** `app/main.py`를 FastAPI 애플리케이션의 메인 진입점으로 구성하고 초기 라우터를 통합했습니다.

## 2. 설정 관리

*   **환경 변수:** `.env` 파일을 사용하여 민감한 설정 값(예: 데이터베이스 연결 문자열, JWT 비밀 키)을 관리하기 위해 `app/core/config.py`를 개발했습니다.
*   **보안 모범 사례:** 민감한 정보가 버전 관리에 커밋되는 것을 방지하기 위해 `.env`를 `.gitignore`에 추가했습니다.

## 3. 사용자 인증 API

*   **비밀번호 해싱:** `app/core/security.py` 내에서 사용자 비밀번호의 안전한 해싱 및 검증을 위해 `passlib`을 통합했습니다.
*   **JWT (JSON 웹 토큰):** 사용자 세션 및 인증 관리를 위한 JWT 생성 및 유효성 검사 로직을 `app/core/security.py` 내에 구현했습니다.
*   **OAuth2.0 비밀번호 플로우:** OAuth2.0 비밀번호 플로우를 기반으로 사용자 로그인 및 JWT 액세스 토큰 발급을 처리하기 위해 인증 API 엔드포인트(`app/api/endpoints/auth.py`)를 개발했습니다.
*   **사용자 CRUD 작업:** 인증 프로세스를 지원하기 위해 사용자 생성, 검색, 업데이트 및 삭제와 관련된 데이터베이스 작업을 캡슐화하는 `app/crud/user.py`를 생성했습니다.

## 4. 조직 및 사용자 관리 API

*   **권한 부여를 위한 의존성 주입:** API 엔드포인트 전반에 걸쳐 사용자 인증 및 역할 기반 권한 부여를 처리하기 위한 재사용 가능한 의존성 주입 함수를 제공하기 위해 `app/api/deps.py`를 생성했습니다.
*   **사용자 등록:** 신규 사용자 등록을 위한 API 엔드포인트를 `app/api/endpoints/users.py`에 구현했습니다.
*   **조직 관리:** 조직 단위 생성 및 검색을 위한 API 엔드포인트를 `app/api/endpoints/organizations.py`에 개발했으며, `app/crud/organization.py`의 해당 CRUD 로직이 이를 지원합니다.

## 5. 테스트 환경 설정 및 초기 디버깅

*   **테스트 스위트 구조:** `pytest` 구성을 위한 `conftest.py`와 테스트 유틸리티 함수를 위한 `tests/utils/user.py`를 포함하는 `tests/` 디렉터리를 확립했습니다.
*   **API 테스트 범위:** 인증, 사용자 관리 및 조직 API에 대한 초기 테스트 케이스(`test_auth.py`, `test_users.py`, `test_organizations.py`)를 작성했습니다.
*   **의존성 해결:** `pytest` 실행 중 발생한 `ModuleNotFoundError`, `PydanticImportError` (`BaseSettings`용), `ImportError` (`email-validator`용)를 포함한 다양한 의존성 관련 문제를 해결하여 `requirements.txt`의 여러 차례 수정으로 이어졌습니다.

## 6. 의존성 관리 도구 마이그레이션 (Poetry)

*   프로젝트 의존성 관리를 위해 `pip`에서 `Poetry`로의 마이그레이션을 시작했습니다.
*   **현재 상태/문제:** `poetry` 명령 경로 문제에 직면했으며, 이를 해결하기 위해 사용자 개입(터미널 재시작)이 필요했습니다.