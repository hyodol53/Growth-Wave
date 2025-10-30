# Task: 정성평가 시스템 개편

**문서 ID:** `task_refactor_qualitative_evaluation`
**작성자:** 프론트엔드 에이전트
**상태:** 제안 (Proposed)

## 1. 개요

본 문서는 사용자의 요구사항에 따라 기존의 단일 점수 기반 정성평가 시스템을 다각화된 평가 항목(정성평가, 부서기여도, 피드백)으로 개편하고, 최종 점수 산출 가중치를 조정하기 위한 백엔드 변경 사항을 기술합니다.

## 2. 변경 필요사항

### 2.1. 데이터베이스 모델 수정

- **대상 파일:** `app/models/evaluation.py`
- **변경 내용:** `QualitativeEvaluation` 모델의 필드를 아래와 같이 수정해야 합니다.
    - **기존:** `score: int` (단일 점수)
    - **변경 후:**
        - `qualitative_score: int` (정성평가 점수, 최대 20점)
        - `department_contribution_score: int` (부서기여도 점수, 최대 10점)
        - `feedback: str` (서술형 피드백)

### 2.2. API 스키마 (Pydantic) 수정

- **대상 파일:** `app/schemas/evaluation.py`
- **변경 내용:** `QualitativeEvaluationCreate`, `QualitativeEvaluationUpdate`, `QualitativeEvaluationInDB` 등의 스키마를 위 모델 변경에 맞춰 수정해야 합니다.
    - **예시 (`QualitativeEvaluationCreate`):**
        ```python
        class QualitativeEvaluationCreate(BaseModel):
            evaluator_id: int
            target_id: int
            project_id: int
            qualitative_score: int
            department_contribution_score: int
            feedback: str
        ```

### 2.3. CRUD 로직 수정

- **대상 파일:** `app/crud/qualitative_evaluation.py`
- **변경 내용:** 정성평가를 생성(`create`), 수정(`update`)하는 CRUD 함수가 새로운 스키마와 모델 필드를 처리하도록 업데이트해야 합니다.

### 2.4. 최종 등급 산출 로직 변경

- **대상 파일:** `app/crud/evaluation_calculator.py` (또는 관련 로직이 있는 파일)
- **변경 내용:** 최종 점수(Final Score)를 계산하는 로직을 아래의 가중치에 맞게 수정해야 합니다.
    - **정성평가 반영 비율:** 30%
    - **프로젝트평가 반영 비율:** 70%
    - **산출 공식:**
        - `정성평가 합산 점수 = qualitative_score + department_contribution_score`
        - `최종 점수 = (프로젝트평가 합산 점수 * 0.7) + (정성평가 합산 점수 / 30 * 100 * 0.3)`
        - *참고: 정성평가 합산 점수는 만점(30점)을 100점 만점으로 환산 후 가중치를 적용해야 합니다.*

## 3. 영향 범위

- **API:** 정성평가 생성/수정/조회 API의 명세가 변경됩니다. (본 문서의 API 명세 변경안 참고)
- **Frontend:** 변경된 API 명세에 맞춰 정성평가 입력 UI 및 데이터 처리 로직 수정이 필요합니다.
- **Database:** 마이그레이션 스크립트 작성이 필요할 수 있습니다.

## 4. API 명세 변경안

(별도 API 문서 파일에 상세히 기술)
