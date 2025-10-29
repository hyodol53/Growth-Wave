# Development Guide

This document provides instructions for setting up the development environment and guidelines for contributing to the project.

## 1. Project Overview

[A brief description of the project will be added here later.]

## 2. Development Environment Setup

### 2.1. Prerequisites

*   Python 3.10
*   Poetry

### 2.2. Installation

1.  **Clone the repository.**
2.  **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```

### 2.3. Running the Application

*   To run the FastAPI application in development mode (with auto-reload):
    ```bash
    poetry run uvicorn app.main:app --reload
    ```

### 2.4. Running Tests

*   To run the test suite:
    ```bash
    poetry run pytest
    ```

## 3. Project Structure

```
.
├── app/                # Main application code
│   ├── api/            # API endpoints
│   ├── core/           # Core components (config, db, security)
│   ├── crud/           # CRUD operations
│   ├── models/         # SQLAlchemy models
│   └── schemas/        # Pydantic schemas
├── docs/               # Documentation
│   ├── ARCHITECTURE.md
│   ├── DEVELOPMENT_GUIDE.md
│   ├── REQUIREMENTS.md
│   └── WORK_PLAN.md
├── tests/              # Tests
├── .gitignore
├── pyproject.toml      # Project metadata and dependencies
└── README.md
```

## 4. 병렬 개발 가이드라인 (Parallel Development Guidelines)

To ensure smooth parallel development, please adhere to the following guidelines.

### 4.1. Code Style

[We will define and enforce code style using tools like Black and isort later.]

### 4.2. 충돌 방지 및 작업 중단 가이드 (Conflict Avoidance & Work Stoppage Guide)

에이전트 간 실시간 의사소통이 불가능하므로, 충돌 가능성을 최소화하고 안전하게 작업을 진행하기 위해 다음 규칙을 반드시 준수해야 합니다.

*   **엄격한 작업 범위 준수**: `WORK_PLAN.md`에 명시된 담당자(Agent)와 작업 범위를 반드시 확인하고, **본인에게 할당된 파일 수정 및 생성 작업만 수행합니다.**

*   **충돌 감지 시 즉시 중단 및 보고**:
    *   다른 에이전트의 작업 범위에 속하는 파일을 수정해야 할 경우
    *   공용 모듈(`app/core`, `app/models` 등)의 수정이 불가피한 경우
    *   계획에 없는 파일을 생성 또는 수정해야 할 경우
    *   **위와 같은 충돌 가능성이 감지되면, 즉시 작업을 중단하고 현재 상황과 필요한 변경 사항을 사용자에게 보고해야 합니다.** 사용자의 결정에 따라 다음 단계를 진행합니다.

### 4.3. 테스트 코드 작성 (Writing Test Code)

*   **테스트 코드 필수 작성**: 모든 백엔드 기능 개발, 수정, 버그 픽스 시에는 반드시 해당 변경 사항을 검증하는 테스트 코드를 작성해야 합니다.
*   **테스트 위치**: 테스트 코드는 `tests/` 디렉토리 하위에 관련 도메인에 맞춰 작성합니다. (예: `tests/api/test_users.py`)
*   **실행**: 새로운 코드가 추가되거나 변경될 때마다 `poetry run pytest`를 실행하여 전체 테스트가 통과하는지 확인해야 합니다.

### 4.4. API 문서 작성 (API Documentation)

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

### 4.5. 신규 기능 추가 시 체크리스트 (Checklist for Adding New Features)

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

## 5. 문서화 가이드라인 (Documentation Guidelines)

프로젝트의 투명성과 지속적인 지식 공유를 위해, 에이전트는 다음 문서화 가이드라인을 준수해야 합니다.

### 5.1. 문서 디렉터리 구조 및 목적

`docs/` 디렉터리는 다음과 같은 하위 디렉터리로 구성되며, 각 디렉터리는 명확한 목적을 가집니다.

*   **`docs/devlog/` (개발 로그):**
    *   **목적:** 특정 기능 개발(`Task`) 단위의 상세한 기술 내역, 마주쳤던 문제, 해결 과정 등을 기록합니다. 다른 개발자가 과거의 작업 내용을 깊이 있게 이해하고 싶을 때 참고하는 '개발 일지' 역할을 합니다.
    *   **작성 시점:** 특정 Task 개발 완료 후 또는 중요한 기술적 결정/문제 해결 시.
    *   **내용:** 기술적 설명, 문제 진술 및 해결책, 관련 코드 스니펫, 아키텍처 다이어그램, 관련 이슈 참조 등.
    *   **파일명 규칙:** `task_ID_short_description.md` (예: `task_3_1_external_account_integration.md`) 또는 `phase_NUMBER_short_description.md` (예: `phase_1_initial_setup_and_auth.md`)
    *   **언어:** 한국어

*   **`docs/history/` (프로젝트 이력):**
    *   **목적:** 완료된 프로젝트 단계(`Phase`)별 주요 성과 및 마일스톤에 대한 역사적 개요를 제공합니다. 프로젝트의 진화 과정을 고수준으로 이해하는 데 도움을 줍니다.
    *   **작성 시점:** 각 Phase 완료 후.
    *   **내용:** 각 개발 단계 요약, 주요 구현 기능 개요, 도전 과제 및 해결책에 대한 고수준 설명, 에이전트 자체 작업 요약 등.
    *   **파일명 규칙:** `phase_NUMBER.md` (예: `phase1.md`)
    *   **언어:** 한국어

*   **`docs/summary/` (프로젝트 요약):**
    *   **목적:** 프로젝트의 현재 상태와 진행 상황에 대한 고수준 요약 정보를 제공합니다. 프로젝트의 현재 초점, 개발 상태 및 주요 예정된 마일스톤을 빠르고 간결하게 파악할 수 있도록 합니다. '대시보드' 또는 '경영진 요약' 역할을 합니다.
    *   **작성 시점:** 프로젝트의 주요 변경 사항 발생 시 또는 주기적인 현황 업데이트 시.
    *   **내용:** 전반적인 프로젝트 상태 및 진행 상황, 현재 우선순위 및 즉각적인 다음 단계, 고수준 아키텍처 개요, 다른 상세 문서에 대한 링크 등.
    *   **파일명 규칙:** `current_status.md` 또는 `project_overview.md` 등 프로젝트의 현재 상태를 나타내는 명확한 이름.
    *   **언어:** 한국어

### 5.2. 문서 작성 원칙

*   **명확성 및 간결성:** 내용은 명확하고 이해하기 쉬워야 하며, 불필요한 정보는 포함하지 않습니다.
*   **정확성:** 모든 정보는 사실에 기반해야 하며, 최신 상태를 유지해야 합니다.
*   **일관성:** 파일명, 제목, 내용 구성 등 모든 문서에서 일관된 형식을 유지합니다.
*   **한국어 사용:** 모든 문서는 한국어로 작성합니다.

### 5.3. 프론트엔드 개발 가이드라인 (Frontend Development Guidelines)

프론트엔드 개발 시 백엔드 API와의 연동 과정에서 발생할 수 있는 문제를 최소화하기 위해 다음 가이드라인을 준수합니다.

*   **실제 존재하는 API만 호출**: 프론트엔드에서 백엔드 API를 호출하기 전에, 해당 API 엔드포인트가 백엔드에 실제로 구현되어 있고 정상적으로 동작하는지 **반드시 확인해야 합니다.** API 문서(`docs/api/`)를 참조하거나 백엔드 개발자와 소통하여 API의 존재 여부 및 명세를 확인합니다.

*   **필요한 API가 없는 경우 작업 중단 및 보고**: 프론트엔드 기능 구현에 필수적인 백엔드 API가 아직 개발되지 않았거나, API 명세가 불분명한 경우, **즉시 프론트엔드 개발 작업을 중단하고 사용자(또는 백엔드 개발자)에게 해당 상황을 보고해야 합니다.** 임의로 API를 가정하여 프론트엔드 코드를 작성하는 것을 금지합니다.

*   **메뉴 및 콘텐츠 한글 작성**: 사용자 인터페이스(UI)의 모든 메뉴 항목, 버튼 텍스트, 페이지 제목, 설명, 오류 메시지 등 사용자에게 노출되는 모든 텍스트 콘텐츠는 **반드시 한국어로 작성해야 합니다.** 이는 한국인 사용자를 위한 서비스 현지화(Localization)의 핵심 요구사항입니다. 기존 영문 텍스트가 있다면 한국어로 적용합니다.

*   **반응형 레이아웃 및 전역 스타일 원칙**:
    *   **전역 스타일 최소화**: `index.css`, `App.css`와 같은 전역 CSS 파일에서는 앱 전체의 너비를 고정(`max-width`)하거나 특정 레이아웃(`display: flex`, `text-align: center` 등)을 강제하는 스타일을 지양합니다. 전역 스타일은 기본적인 폰트, 색상, 최소 너비 설정에만 사용하고, 페이지별 레이아웃은 각 컴포넌트 내에서 `Material-UI`의 `Box`, `Grid` 등을 사용하여 독립적으로 제어합니다.
    *   **유연한 너비 사용**: `DataGrid`의 열(column)이나 컨테이너의 너비를 설정할 때, 고정된 `px` 값 대신 `flex`와 `minWidth` 속성을 사용하여 화면 크기에 따라 자연스럽게 너비가 조절되도록 구현합니다.

*   **커스텀 파일 입력 컴포넌트 패턴**:
    *   브라우저 기본 `<input type="file">`은 스타일링이 어렵고 레이아웃 문제를 유발할 수 있으므로 직접 사용을 지양합니다.
    *   대신, `<input type="file">`을 `style={{ display: 'none' }}`으로 숨기고, `Material-UI`의 `Button`을 클릭했을 때 숨겨진 `input`을 프로그래매틱하게(`ref.current.click()`) 실행하는 방식을 사용합니다.
    *   선택된 파일의 이름은 `Typography` 컴포넌트 등을 이용해 별도로 표시하여 사용자 경험을 향상시킵니다. 이 패턴은 일관된 UI를 제공하고 레이아웃 문제를 근본적으로 방지합니다.

#### 5.3.1. 프론트엔드 개발 최종 검증 절차

모든 프론트엔드 기능 구현, 수정, 리팩토링 작업 완료 시, 다음 검증 절차를 반드시 수행해야 합니다.

*   **빌드 성공 확인 (필수)**: 개발을 완료했다고 판단하기 전에, 반드시 `npm run build` 명령어를 실행하여 프로젝트가 성공적으로 빌드되는지 확인해야 합니다. 컴파일 오류가 하나라도 발생하는 경우, 모든 오류를 해결하기 전까지 개발을 완료한 것으로 간주하지 않습니다.

*   **가정 금지 및 코드 확인**: 로컬 파일 시스템에 접근할 수 있는 경우, 코드의 내용이나 구조에 대해 절대 가정해서는 안 됩니다. 특정 함수의 존재 여부, 변수명, 타입 정의, 컴포넌트의 props 등 코드와 관련된 모든 정보는 반드시 해당 파일을 직접 읽어 확인해야 합니다. 이를 통해 추측이 아닌 사실에 기반한 정확한 코드를 작성합니다.
