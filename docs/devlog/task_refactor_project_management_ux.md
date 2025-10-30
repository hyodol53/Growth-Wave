# 개발 로그: 프로젝트 관리 UX 개편 및 평가 기간 연동

- **Task ID:** (미지정, 프론트엔드 UX 개편 관련)
- **작성자:** 프론트엔드 에이전트
- **작성일:** 2025-10-30

## 1. 개발 목표

기존의 프로젝트 관리 방식은 '평가 기간'과 명시적인 관계가 설정되어 있지 않아 데이터 정합성 및 사용자 경험(UX)에 문제가 있었다. 이번 Task의 목표는 다음과 같다.

1.  **데이터 모델 개선 제안:** 프로젝트가 특정 평가 기간에 명시적으로 귀속되도록 백엔드 팀에 데이터 모델 변경을 요청한다. (`FR-A-6.1`, `FR-A-6.3` 관련)
2.  **평가 기간 중심 UX 구현:** 관리자가 '평가 기간'을 먼저 선택하면, 해당 기간에 속한 프로젝트만 조회하고 관리할 수 있도록 프론트엔드 UI를 개편한다. (`FR-A-6.4` 신규 반영)
3.  **API 연동:** 변경된 백엔드 API 명세에 맞춰 프론트엔드의 API 호출 로직을 수정한다.

## 2. 개발 내역

### 2.1. 백엔드 변경 요청 및 API 문서 수정

- **백엔드 요청 문서 생성:**
    - `docs/request_for_backend_refactor_project_evaluation_period.md` 파일을 생성하여, `Project` 모델에 `evaluation_period_id`를 추가하고 관련 API를 수정해달라는 요청사항을 상세히 기술함.
- **API 문서 업데이트:**
    - `docs/api/projects/create_project.md`: 프로젝트 생성 시 `evaluation_period_id`를 필수로 받도록 수정.
    - `docs/api/projects/get_projects.md`: `evaluation_period_id`를 쿼리 파라미터로 받아 프로젝트를 필터링하는 기능을 명시.

### 2.2. 프론트엔드 UI 및 로직 수정

- **`frontend/src/pages/Admin/ProjectManagementPage.tsx` 수정:**
    - **평가 기간 조회:** 페이지 진입 시, `api.evaluationPeriods.getEvaluationPeriods()`를 호출하여 전체 평가 기간 목록을 가져오는 기능을 추가함.
    - **평가 기간 선택 UI:** 가져온 평가 기간 목록을 보여주는 MUI `Select` (드롭다운) 컴포넌트를 추가함. 사용자가 평가 기간을 선택하면 `selectedEvaluationPeriod` 상태가 업데이트됨.
    - **조건부 프로젝트 조회:** `selectedEvaluationPeriod` 상태가 변경될 때마다 `useEffect`를 트리거하여, `api.projects.getProjects({ evaluation_period_id: periodId })`를 호출. 선택된 평가 기간에 속한 프로젝트 목록만 서버에 요청하고 화면에 렌더링하도록 수정함.
    - **'Add Project' 버튼 비활성화 로직:** 평가 기간이 선택되지 않았을 경우, 새 프로젝트를 추가할 수 없도록 버튼을 비활성화 처리하여 UX를 개선함.

- **`frontend/src/components/Admin/ProjectDialog.tsx` 수정:**
    - **평가 기간 선택 기능 추가:** 프로젝트 생성/수정 다이얼로그 내에 `evaluationPeriods` 목록을 보여주는 `Select` 컴포넌트를 추가함.
    - **기본값 설정:** 새 프로젝트 생성 시, `ProjectManagementPage`에서 선택된 평가 기간 ID(`selectedEvaluationPeriodId`)가 자동으로 설정되도록 구현함.
    - **API 요청 데이터 수정:** 'Save' 버튼 클릭 시, `evaluation_period_id`를 포함한 프로젝트 데이터를 부모 컴포넌트로 전달하여 생성/수정 API가 호출되도록 수정함.

### 2.3. 타입 정의(Schema) 및 API 서비스 수정

- **`frontend/src/schemas/project.ts`:** `Project`, `ProjectCreate`, `ProjectUpdate` 인터페이스에 `evaluation_period_id: number;` 필드를 추가함.
- **`frontend/src/schemas/evaluation.ts`:** `EvaluationPeriod` 인터페이스를 추가하고, 빌드 과정에서 발견된 다른 누락된 타입들을 복원함.
- **`frontend/src/schemas/index.ts`:** `evaluation.ts`의 타입들을 export하도록 추가함.
- **`frontend/src/services/api.ts`:**
    - `projects.getProjects` 함수가 `evaluation_period_id`를 파라미터로 받을 수 있도록 수정함.
    - `evaluationPeriods.getEvaluationPeriods` 함수를 새로 추가하여 평가 기간 목록을 조회하는 API 호출을 정의함.

## 3. 문제 해결 과정

개발 과정에서 다수의 타입스크립트 컴파일 오류가 발생했으며, 이를 해결하기 위해 다음과 같은 과정을 거쳤다.

1.  **초기 진단:** `evaluation.ts` 파일을 잘못 덮어쓰면서 프로젝트 전반의 타입 정의가 깨진 것을 확인함.
2.  **스키마 복원 및 정리:** 백업된 `evaluation.ts` 파일 내용을 기반으로 중복 선언된 타입(`UserRole` 등)을 제거하고, 다른 컴포넌트와의 불일치(`EvaluationWeight` 필드명 등)를 수정하며 스키마 파일을 점진적으로 안정화시킴.
3.  **잘못된 Import 경로 수정:** `user.ts` 등 다른 스키마 파일에서 `evaluation.ts`의 타입을 잘못 참조하던 부분을 바로잡음.
4.  **MUI Grid 컴포넌트 오류 해결:** 수차례의 시도 끝에, `ProjectDialog.tsx`에서 `GridLegacy as Grid`를 사용하도록 수정하여 고질적인 `Grid` 컴포넌트 관련 컴파일 오류를 최종 해결함.
5.  **반복적인 빌드:** 각 수정 단계마다 `npm run build`를 실행하여 오류가 점차 줄어드는 것을 확인하며 체계적으로 문제를 해결함.

## 4. 결과

- 프로젝트 관리 기능이 '평가 기간' 중심으로 동작하도록 UX가 성공적으로 개편됨.
- 백엔드 API 명세 변경에 맞춰 프론트엔드 코드가 모두 수정되었으며, 최종적으로 모든 컴파일 오류를 해결하여 빌드에 성공함.
- 관련 요구사항(`FR-A-6.1`, `FR-A-6.3`, `FR-A-6.4`)이 모두 충족됨.
