
# Task 6.2: 프로젝트 관리 UI 개발

`WORK_PLAN.md`의 **Task 6.2** 요구사항에 따라, 실장 및 관리자가 프로젝트를 관리(조회, 생성, 수정, 삭제)하고 프로젝트 멤버를 배정할 수 있는 프론트엔드 UI 개발을 완료했습니다.

## 1. 라우팅 및 네비게이션 설정

- **`AuthorizedRoute.tsx` 컴포넌트 신설**: 기존의 `AdminRoute`를 대체하여, `admin`과 `dept_head` 등 여러 역할을 배열로 받아 권한을 검사할 수 있는 재사용 가능한 `AuthorizedRoute` 컴포넌트를 구현했습니다.
- **`Layout.tsx` 수정**: 네비게이션 바의 'Admin' 섹션을 'Management'로 변경하고, `admin` 또는 `dept_head` 역할의 사용자에게 'Organization' 및 'Projects' 메뉴가 보이도록 수정했습니다.
- **`App.tsx` 수정**: `/admin/projects` 경로를 추가하고, `AuthorizedRoute`를 사용하여 `admin`과 `dept_head` 역할의 사용자만 접근할 수 있도록 보호했습니다.

## 2. 프로젝트 관리 페이지 구현 (`ProjectManagementPage.tsx`)

- **데이터 조회**: 페이지 로딩 시 `Promise.all`을 사용하여 프로젝트, 사용자, 조직 목록을 병렬로 조회합니다.
- **UI 구현**: MUI의 `DataGrid`를 사용하여 프로젝트 목록을 테이블 형태로 표시합니다. 각 행에는 프로젝트 정보와 함께 수정, 삭제, 멤버 관리를 위한 액션 버튼을 포함시켰습니다.
- **API 연동**: `services/api.ts`에 프로젝트 CRUD(`getProjects`, `createProject`, `updateProject`, `deleteProject`) 및 멤버 관리(`getProjectMembers`, `setProjectMemberWeights`)를 위한 함수를 추가했습니다.

## 3. 프로젝트 생성/수정 기능 구현 (`ProjectDialog.tsx`)

- **다이얼로그 UI**: 프로젝트의 이름, 설명, 기간, PM, 소유 조직을 입력받는 폼을 포함한 재사용 가능한 다이얼로그 컴포넌트를 구현했습니다.
- **상태 관리**: `useState`와 `useEffect`를 사용하여 폼 데이터를 관리하고, 부모 컴포넌트(`ProjectManagementPage`)와의 데이터 동기화를 처리합니다.
- **저장 로직**: '저장' 버튼 클릭 시, `onSave` 콜백 함수를 통해 입력된 데이터를 부모 컴포넌트로 전달하여 API(생성 또는 수정) 호출을 트리거합니다.

## 4. 프로젝트 멤버 관리 기능 구현 (`ProjectMemberDialog.tsx`)

- **멤버 관리 UI**: 특정 프로젝트의 현재 멤버 목록을 표시하고, 새로운 멤버를 추가하거나 기존 멤버를 삭제하는 UI를 구현했습니다.
- **참여 비중 관리**: 각 멤버의 참여 비중(%)을 `TextField`로 수정할 수 있으며, 전체 비중의 합계가 실시간으로 표시됩니다.
- **유효성 검사**: 멤버 비중의 총합이 정확히 100%가 아닐 경우, 경고 메시지를 표시하고 저장 버튼을 비활성화하여 데이터의 정합성을 보장합니다.
- **API 가정 및 예외 처리**: 백엔드에 프로젝트 멤버를 조회하는 API(`getProjectMembers`)가 아직 구현되지 않았을 가능성을 염두에 두고, 해당 API 호출 실패 시 사용자에게 기능이 미완성일 수 있다는 에러 메시지를 표시하도록 방어적으로 구현했습니다.

## 결론

이로써 관리자와 실장이 프로젝트의 전체 라이프사이클을 관리하고 멤버들의 참여 비중을 설정할 수 있는 모든 UI 기능 개발이 완료되었습니다. Task 6.2가 성공적으로 마무리되었습니다.
