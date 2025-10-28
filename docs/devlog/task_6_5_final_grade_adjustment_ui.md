# Task 6.5: 최종 등급 조정 UI 개발

`WORK_PLAN.md`의 **Task 6.5** 요구사항에 따라, 실장 및 관리자가 하위 조직원의 최종 등급을 조정할 수 있는 프론트엔드 UI 개발을 완료했습니다.

## 1. 라우팅 및 네비게이션 설정

- **경로 추가**: `App.tsx`에 관리자 및 실장 전용 경로인 `/admin/grade-adjustment`를 추가하고, `AuthorizedRoute` 컴포넌트를 사용하여 `admin` 및 `dept_head` 역할의 사용자만 접근할 수 있도록 보호했습니다.
- **메뉴 추가**: `Layout.tsx`의 'Management' 섹션에 'Grade Adjustment' 메뉴 항목을 추가하여, 권한이 있는 사용자에게만 해당 메뉴가 보이도록 설정했습니다.

## 2. API 연동 및 스키마 정의

- **스키마 확장**: `schemas/evaluation.ts` 파일에 `FinalEvaluation`, `ManagerEvaluationView`, `GradeAdjustmentRequest` 등 등급 조정 기능에 필요한 TypeScript 인터페이스를 추가했습니다.
- **API 함수 추가**: `services/api.ts` 파일에 다음 두 가지 API 호출 함수를 구현했습니다.
    - `getEvaluationResultForUser(userId)`: 특정 사용자의 상세 평가 결과를 조회합니다 (`GET /evaluations/{userId}/result`).
    - `adjustGrades(adjustments)`: 변경된 등급 정보를 서버에 제출합니다 (`POST /evaluations/adjust-grades`).

## 3. 등급 조정 페이지 구현 (`FinalGradeAdjustmentPage.tsx`)

- **데이터 조회**: 페이지 로딩 시, `getMySubordinates` API를 통해 자신의 하위 조직원 목록을 가져온 후, `Promise.all`을 사용하여 각 조직원의 상세 평가 정보를 병렬로 조회하도록 구현했습니다.
- **UI 구현**:
    - MUI의 `DataGrid`를 사용하여 조직원 목록, 최종 점수, 현재 등급, 조정 등급을 테이블 형태로 표시했습니다.
    - 'Adjusted Grade' 열은 `select` 드롭다운 메뉴로 구현하여 관리자가 직관적으로 등급(S, A, B+, B, B-, C, D)을 변경할 수 있도록 했습니다.
- **유효성 검사**:
    - `FR-A-4.4` 요구사항에 따라, B+ 등급을 받은 인원수와 B- 등급을 받은 인원수가 동일해야 한다는 규칙을 프론트엔드에서 실시간으로 검증하는 로직을 구현했습니다.
    - 규칙이 위반될 경우, 사용자에게 경고 메시지를 표시하고 'Save Changes' 버튼을 비활성화하여 잘못된 데이터 제출을 방지합니다.
- **상태 관리 및 피드백**:
    - 데이터 로딩, 오류 발생, 저장 성공 등 비동기 작업의 상태를 사용자에게 명확히 전달하기 위해 `Alert` 및 `Snackbar` 컴포넌트를 활용했습니다.

## 결론

이로써 관리자와 실장이 시스템을 통해 산출된 평가 등급을 최종적으로 검토하고 조정할 수 있는 모든 UI 기능 개발이 완료되었습니다. Task 6.5가 성공적으로 마무리되었습니다.
