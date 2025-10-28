# Task 6.4: 평가 진행 UI - Mock 데이터 API 연동 전환

- **작업 일시:** 2025-10-28
- **담당자:** Agent-Frontend
- **상태:** 완료

## 1. 작업 개요

`WORK_PLAN.md`의 `Task 6.4`에 따라, `MyEvaluationsPage.tsx` 컴포넌트의 평가 진행 UI를 완성하는 것을 목표로 한다.

기존에는 백엔드의 `GET /projects/{project_id}/members`와 `GET /users/me/subordinates` API가 구현되지 않아, 임시 Mock 데이터를 사용하여 UI 컴포넌트의 레이아웃과 기본 동작을 구현해 둔 상태였다.

본 작업의 핵심은 백엔드 개발이 완료됨에 따라, 이 Mock 데이터를 실제 API 호출 로직으로 전환하고 데이터를 동적으로 연동하는 것이다.

## 2. 주요 변경 사항

### 2.1. API 서비스 및 스키마 확장 (`api.ts`, `schemas/`)

- **`project_id` 문제 해결:** 기존에 `GET /users/me/history` API가 `project_name`만 반환하여 평가 대상을 특정할 수 없었던 문제를 해결하기 위해, 백엔드에서 `project_id`를 응답에 포함하도록 수정했다.
- **스키마 정의:**
    - `schemas/user.ts`: `history` API의 응답을 처리하기 위해 `UserHistoryItem` 인터페이스를 추가했다.
    - `schemas/project.ts`: `members` API의 상세 응답을 처리하기 위해 `ProjectMemberDetails` 인터페이스를 추가했다.
- **API 함수 추가 및 정리:**
    - `services/api.ts`: `getUserHistory` 함수를 추가하고, 기존에 중복 정의되었던 `getProjectMembers` 함수를 정리하여 API 호출 로직을 일원화했다.

### 2.2. `MyEvaluationsPage.tsx` 리팩토링

- **Mock 데이터 제거:** 컴포넌트 상단에 하드코딩되어 있던 `mockMySubordinates`, `mockProjects`, `mockProjectMembers` 배열을 모두 삭제했다.
- **상태 관리 추가:** API로부터 받아온 데이터를 저장하기 위해 `subordinates`, `projectsWithMembers` 등의 React 상태(state)를 추가했다.
- **데이터 로딩 로직 구현:**
    - `useEffect` 훅 내에서 다음의 순서로 데이터를 비동기적으로 로딩하도록 구현했다.
        1. `getCurrentUser`: 현재 로그인한 사용자 정보를 가져온다.
        2. `getUserHistory`: 사용자가 참여 중인 프로젝트 목록(`project_id` 포함)을 가져온다.
        3. `getMySubordinates`: 사용자가 팀장/실장일 경우, 정성평가 대상인 하위 조직원 목록을 가져온다.
        4. `getProjectMembers`: `Promise.all`을 사용하여 참여 중인 모든 프로젝트의 멤버 목록을 병렬로 가져온다.
- **동적 UI 렌더링:**
    - API를 통해 가져온 실제 데이터를 기반으로 '정성평가', '동료평가', 'PM 평가' 등의 평가 태스크(Task) 카드를 동적으로 생성하도록 로직을 수정했다.
    - 평가 다이얼로그(Dialog) 컴포넌트에 Mock 데이터 대신 실제 프로젝트 멤버 및 하위 조직원 데이터를 전달하도록 수정했다.

## 3. 결과

- `MyEvaluationsPage`는 이제 백엔드 API와 완전히 연동되어, 로그인한 사용자의 권한과 프로젝트 참여 현황에 따라 실제 진행해야 할 평가 목록을 정확하게 보여준다.
- Mock 데이터 의존성을 제거하여 백엔드 변경에 유연하게 대응할 수 있는 코드 구조를 완성했다.
- TypeScript 타입 검사를 통과하여 코드의 안정성을 확보했다.

이로써 `Task 6.4`의 UI 개발 및 백엔드 연동 작업이 완료되었다.