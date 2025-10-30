# 공통 개발 가이드라인

이 문서는 프로젝트에 기여하는 모든 에이전트(백엔드, 프론트엔드 등)가 공통으로 준수해야 할 가이드라인을 정의합니다.

## 1. 프로젝트 개요

[A brief description of the project will be added here later.]

## 2. 프로젝트 구조

```
.
├── app/                # Main application code (Backend)
├── docs/               # Documentation
├── frontend/           # Frontend application code
├── tests/              # Tests
├── .gitignore
├── pyproject.toml      # Project metadata and dependencies (Backend)
├── package.json        # Project metadata and dependencies (Frontend)
└── README.md
```

## 3. 병렬 개발 가이드라인 (Parallel Development Guidelines)

에이전트 간 실시간 의사소통이 불가능하므로, 충돌 가능성을 최소화하고 안전하게 작업을 진행하기 위해 다음 규칙을 반드시 준수해야 합니다.

### 3.1. Code Style

[We will define and enforce code style using tools like Black and isort later.]

### 3.2. 충돌 방지 및 작업 중단 가이드 (Conflict Avoidance & Work Stoppage Guide)

*   **엄격한 작업 범위 준수**: `WORK_PLAN.md`에 명시된 담당자(Agent)와 작업 범위를 반드시 확인하고, **본인에게 할당된 파일 수정 및 생성 작업만 수행합니다.**

*   **충돌 감지 시 즉시 중단 및 보고**:
    *   다른 에이전트의 작업 범위에 속하는 파일을 수정해야 할 경우
    *   공용 모듈의 수정이 불가피한 경우 (예: 백엔드의 `app/core`, `app/models`)
    *   계획에 없는 파일을 생성 또는 수정해야 할 경우
    *   **위와 같은 충돌 가능성이 감지되면, 즉시 작업을 중단하고 현재 상황과 필요한 변경 사항을 사용자에게 보고해야 합니다.** 사용자의 결정에 따라 다음 단계를 진행합니다.

## 4. 문서화 가이드라인 (Documentation Guidelines)

프로젝트의 투명성과 지속적인 지식 공유를 위해, 에이전트는 다음 문서화 가이드라인을 준수해야 합니다.

### 4.1. 문서 디렉터리 구조 및 목적

`docs/` 디렉터리는 다음과 같은 하위 디렉터리로 구성되며, 각 디렉터리는 명확한 목적을 가집니다.

*   **`docs/devlog/` (개발 로그):**
    *   **목적:** 특정 기능 개발(`Task`) 단위의 상세한 기술 내역, 마주쳤던 문제, 해결 과정 등을 기록합니다. 다른 개발자가 과거의 작업 내용을 깊이 있게 이해하고 싶을 때 참고하는 '개발 일지' 역할을 합니다.
    *   **작성 시점:** 특정 Task 개발 완료 후 또는 중요한 기술적 결정/문제 해결 시.
    *   **파일명 규칙:** `task_ID_short_description.md` 또는 `phase_NUMBER_short_description.md`
    *   **언어:** 한국어

*   **`docs/history/` (프로젝트 이력):**
    *   **목적:** 완료된 프로젝트 단계(`Phase`)별 주요 성과 및 마일스톤에 대한 역사적 개요를 제공합니다. 프로젝트의 진화 과정을 고수준으로 이해하는 데 도움을 줍니다.
    *   **작성 시점:** 각 Phase 완료 후.
    *   **파일명 규칙:** `phase_NUMBER.md`
    *   **언어:** 한국어

*   **`docs/summary/` (프로젝트 요약):**
    *   **목적:** 프로젝트의 현재 상태와 진행 상황에 대한 고수준 요약 정보를 제공합니다. '대시보드' 또는 '경영진 요약' 역할을 합니다.
    *   **작성 시점:** 프로젝트의 주요 변경 사항 발생 시 또는 주기적인 현황 업데이트 시.
    *   **파일명 규칙:** `current_status.md` 등
    *   **언어:** 한국어

### 4.2. 문서 작성 원칙

*   **명확성 및 간결성:** 내용은 명확하고 이해하기 쉬워야 하며, 불필요한 정보는 포함하지 않습니다.
*   **정확성:** 모든 정보는 사실에 기반해야 하며, 최신 상태를 유지해야 합니다.
*   **일관성:** 파일명, 제목, 내용 구성 등 모든 문서에서 일관된 형식을 유지합니다.
*   **한국어 사용:** 모든 문서는 한국어로 작성합니다.
