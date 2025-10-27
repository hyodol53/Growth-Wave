
# Phase 6: Track A - 공정한 평가 시스템 UI 개발

`WORK_PLAN.md`의 Phase 6 목표에 따라, 공정한 평가 시스템(Track A) 관련 프론트엔드 UI 개발을 진행합니다.

---

## 완료된 작업

- **Task 6.1: 조직/인원 관리 UI 개발 (완료)**
  - **요구사항:** `FR-A-1.4, 1.5, 1.6`
  - 관리자가 조직과 사용자를 조회, 생성, 수정, 삭제할 수 있는 페이지를 구현했습니다.
  - **주요 구현 내용**:
    - UI 개발을 위해 **MUI(Material-UI)** 라이브러리를 도입했습니다.
    - 관리자 역할 기반의 **전용 라우트(`AdminRoute`)** 및 **동적 네비게이션 메뉴**를 구현했습니다.
    - 조직도(`TreeView`)와 사용자 목록(`DataGrid`) UI를 구현하고, 생성/수정/삭제(CUD) 기능을 다이얼로그(Dialog) 폼과 연동하여 완성했습니다.
  - 상세 개발 내역은 [../devlog/task_6_1_org_user_management_ui.md](../devlog/task_6_1_org_user_management_ui.md) 문서를 참고하세요.

- **Task 6.2: 프로젝트 관리 UI 개발 (완료)**
  - **요구사항:** `FR-A-6.x`
  - 실장 및 관리자가 프로젝트를 조회, 생성, 수정, 삭제하고 멤버를 배정할 수 있는 페이지를 구현했습니다.
  - **주요 구현 내용**:
    - `admin`과 `dept_head` 역할을 모두 처리할 수 있는 재사용 가능한 **`AuthorizedRoute`** 컴포넌트를 구현했습니다.
    - 프로젝트 목록을 표시하는 `DataGrid`와 생성/수정을 위한 `ProjectDialog`를 구현했습니다.
    - 프로젝트 멤버를 배정하고 참여 비중(%)을 관리하는 `ProjectMemberDialog`를 구현했으며, 총합 100% 유효성 검사 로직을 포함했습니다.
  - 상세 개발 내역은 [../devlog/task_6_2_project_management_ui.md](../devlog/task_6_2_project_management_ui.md) 문서를 참고하세요.
