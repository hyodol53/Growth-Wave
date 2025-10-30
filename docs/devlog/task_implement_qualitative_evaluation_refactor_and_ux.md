# Task: 정성평가 시스템 개편 및 UX 개선 API 구현 완료

**문서 ID:** `task_implement_qualitative_evaluation_refactor_and_ux`
**작성자:** 백엔드 에이전트
**상태:** 완료 (Done)

## 1. 개요

본 문서는 프론트엔드 팀의 요구사항(`task_refactor_qualitative_evaluation.md`, `task_refactor_qualitative_evaluation_ux.md`)에 따라 진행된 정성평가 시스템의 백엔드 개편 작업 내역을 기록한다. 주요 작업 범위는 데이터 모델 변경, 최종 점수 산출 로직 수정, 그리고 역할 기반의 평가 대상 조회 API 구현을 포함한다.

## 2. 주요 변경 사항

### 2.1. 정성평가 데이터 모델 및 스키마 확장

- **목적:** 단일 점수 체계를 다각화된 평가 항목으로 확장
- **변경 파일:**
    - `app/models/evaluation.py`: `QualitativeEvaluation` 모델의 `score` 필드를 `qualitative_score`(최대 20점), `department_contribution_score`(최대 10점)로 분리하고, `comment`를 `feedback`으로 변경했다.
    - `app/schemas/evaluation.py`: 모델 변경에 맞춰 `QualitativeEvaluationBase` 등 관련 Pydantic 스키마를 수정하고, `Field`를 사용하여 각 점수 항목에 대한 유효성 검증(0-20, 0-10)을 추가했다.
- **영향:**
    - 정성평가 생성(`POST`) API의 요청 본문이 새로운 스키마를 따르게 되었다.
    - 데이터베이스 변경을 위해 마이그레이션 스크립트(`migrations/004_...`)를 추가했다.

### 2.2. 최종 점수 산출 로직 수정

- **목적:** 새로운 평가 정책(프로젝트 평가 70%, 정성평가 30%) 적용
- **변경 파일:** `app/crud/evaluation_calculator.py`
- **변경 내용:**
    - `calculate_and_store_final_scores` 함수의 로직을 수정했다.
    - 정성평가 점수는 `qualitative_score`와 `department_contribution_score`의 합을 100점 만점으로 환산 후 30% 가중치를 적용한다.
    - 프로젝트 평가는 동료/PM 평가 점수를 DB에 설정된 가중치에 따라 합산한 후 70% 가중치를 적용한다.

### 2.3. 정성평가 대상 조회 API 구현 (`GET`)

- **목적:** 그리드 기반의 정성평가 UX를 지원하기 위해 평가 대상 목록과 기제출된 데이터를 조회하는 API 제공
- **엔드포인트:** `GET /api/v1/evaluations/qualitative-evaluations/`
- **주요 구현 내용:**
    - **스키마 추가 (`app/schemas/evaluation.py`):** API 응답을 위한 `MemberToEvaluateQualitatively`, `QualitativeEvaluationData` 스키마를 추가했다.
    - **CRUD 함수 추가 (`app/crud/qualitative_evaluation.py`):** `get_members_to_evaluate` 함수를 구현했다.
        - **역할 기반 필터링:** 요청자의 역할(`TEAM_LEAD`, `DEPT_HEAD`)에 따라 평가 대상 목록을 동적으로 필터링한다.
        - **데이터 조회:** `LEFT JOIN`을 사용하여 평가 대상의 정보와 함께, 현재 평가자가 이전에 제출한 평가 데이터가 있는 경우 함께 조회한다.
    - **API 엔드포인트 구현 (`app/api/endpoints/evaluations.py`):**
        - CRUD 함수를 호출하여 데이터를 조회한다.
        - 조회된 데이터를 바탕으로 전체 평가 진행 상태(`NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`)를 계산하여 최종 응답을 구성한다.

### 2.4. 사용자 모델에 상급자(reports_to) 관계 추가

- **목적:** 역할 기반 필터링 로직 및 테스트 코드에서 상하위 관계를 명확히 정의하기 위함
- **변경 파일:**
    - `app/models/user.py`: `User` 모델에 `reports_to` 컬럼과 `manager`/`subordinates`의 자기 참조 관계를 추가했다.
    - `app/schemas/user.py`: `UserCreate` 스키마에 `reports_to` 필드를 추가했다.
    - `app/crud/user.py`: `create` 함수가 `reports_to` 값을 처리하도록 수정했다.
- **영향:**
    - 사용자 생성 시 상급자를 지정할 수 있게 되었다.
    - 데이터베이스 변경을 위해 마이그레이션 스크립트(`migrations/005_...`)를 추가했다.
    - 이 변경으로 인해 실패하던 `test_qualitative_evaluations.py` 테스트가 정상적으로 동작하게 되었다.

## 3. 테스트

- 기존의 최종 점수 계산 테스트(`test_final_evaluations.py`)를 새로운 계산 로직에 맞게 수정했다.
- 정성평가 API의 변경 사항을 검증하기 위해 `test_qualitative_evaluations.py` 테스트 코드를 수정 및 추가했다.
- 모든 관련 테스트가 통과하는 것을 확인했다.
