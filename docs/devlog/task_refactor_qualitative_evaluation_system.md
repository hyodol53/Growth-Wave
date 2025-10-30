# Task: 정성평가 시스템 종합 개편 (점수, UX, 정책)

**문서 ID:** `task_refactor_qualitative_evaluation_system`
**작성자:** 프론트엔드 에이전트
**상태:** 완료 (Done)

## 1. 개요

본 문서는 여러 단계에 걸쳐 진행된 정성평가 시스템의 종합적인 개편 작업 내역을 기록합니다. 작업은 크게 세 가지 축으로 진행되었습니다: (1) 평가 항목 및 점수 비중 변경, (2) 프로젝트 평가와 동일한 사용자 경험(UX)으로의 전면 개편, (3) 평가자의 역할에 따른 평가 대상 필터링 정책 도입.

## 2. 주요 작업 내역

### 2.1. 평가 항목 및 점수 로직 변경 (1단계)

- **요구사항:** 기존의 100점 만점 단일 정성평가 항목을 아래와 같이 세분화하고, 최종 점수에서 30%의 비중을 차지하도록 변경.
    - 정성평가 점수 (최대 20점)
    - 부서기여도 점수 (최대 10점)
    - 서술형 피드백
- **조치:**
    - 백엔드 팀에 데이터베이스 모델, 스키마, 최종 점수 산출 로직 변경을 요청하는 기술 문서(`task_refactor_qualitative_evaluation.md`)를 작성했습니다.
    - 변경될 `POST /qualitative-evaluations` API 명세를 업데이트했습니다.
    - 프론트엔드에서는 `schemas/evaluation.ts`의 관련 타입을 수정하고, 평가 입력 UI(`QualitativeEvaluationDialog.tsx`)를 새로운 항목에 맞게 변경했습니다.

### 2.2. UX 전면 개편 및 정책 도입 (2단계)

- **요구사항:**
    1.  **UX 통일:** 다이얼로그 팝업 방식이 아닌, 프로젝트 평가처럼 그리드(표) 내에서 직접 수정하고 제출하는 방식으로 변경.
    2.  **데이터 유지:** 이미 제출한 평가 내역이 그리드에 표시되고, 수정 및 재제출이 가능해야 함.
    3.  **역할 기반 정책:** 팀장은 모든 팀원을, 실장은 하위 구성원 중 팀장급만 평가하도록 로직 변경.
- **조치:**
    - **백엔드 API 추가 요청:**
        - 역할 기반 필터링 로직과 기제출 내역 조회를 담당하는 `GET /evaluations/qualitative-evaluations/` API를 새롭게 설계하고, 기술 문서(`task_refactor_qualitative_evaluation_ux.md`)와 API 명세서(`get_qualitative_evaluations.md`)를 작성하여 백엔드 팀에 전달했습니다.
    - **프론트엔드 리팩토링:**
        - 신규 API 스키마(`QualitativeEvaluationData`)를 `schemas/evaluation.ts`에 추가했습니다.
        - `PeerEvaluationGrid`와 유사한 `QualitativeEvaluationGrid.tsx` 컴포넌트를 신규 생성하여, 데이터 조회, 입력, 수정, 제출 기능을 모두 구현했습니다.
        - `MyEvaluationsPage.tsx`에서 기존 카드/다이얼로그 로직을 모두 제거하고, 신규 그리드 컴포넌트를 렌더링하도록 수정했습니다.
        - 더 이상 사용하지 않는 `QualitativeEvaluationCard.tsx`와 `QualitativeEvaluationDialog.tsx` 파일을 삭제하여 코드를 정리했습니다.
    - **요구사항 문서 업데이트:** 변경된 역할 기반 평가 정책을 `REQUIREMENTS.md` 문서(FR-A-3.5)에 명확히 반영했습니다.

### 2.3. 안정화 및 최종 수정

- **빌드 오류 해결:**
    - 스키마 리팩토링 과정에서 발생했던 다수의 타입 참조 오류를 해결했습니다. 특히, `schemas/index.ts` 파일의 수정을 최소화하는 방향으로 `services/api.ts`의 import 방식을 수정하여 문제를 해결했습니다.
- **UX 개선:**
    - 평가 진행 상태(`status`)에 따라 제출 버튼의 텍스트가 '제출' 또는 '수정 제출'로 동적으로 변경되도록 `QualitativeEvaluationGrid.tsx` 컴포넌트를 개선했습니다.

## 3. 결론

정성평가 기능은 이제 프로젝트 평가와 일관된 사용자 경험을 제공하며, 새로운 비즈니스 정책을 완벽하게 지원합니다. 백엔드와의 명확한 API 설계를 통해 역할을 분담하고, 프론트엔드에서는 컴포넌트 기반의 재사용 가능한 구조로 기능을 구현했습니다.
