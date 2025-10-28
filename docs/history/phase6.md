
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

- **Task 6.3: 평가 설정 UI 개발 (완료)**
  - **요구사항:** `FR-A-2.1, 2.2, 2.3`
  - 관리자가 평가 주기, 등급 비율, 평가 항목별 가중치를 관리할 수 있는 페이지를 구현했습니다.
  - **주요 구현 내용**:
    - 탭(Tabs)을 사용하여 세 가지 다른 설정(주기, 비율, 가중치)을 관리하는 UI를 구성했습니다.
    - 각 설정에 대한 조회(`DataGrid`), 생성/수정(`Dialog`), 삭제 기능을 모두 구현하여 관리의 편의성을 높였습니다.
  - 상세 개발 내역은 [../devlog/task_6_3_evaluation_settings_ui.md](../devlog/task_6_3_evaluation_settings_ui.md) 문서를 참고하세요.

- **Task 6.4: 평가 진행 UI 개발 (완료)**
  - **요구사항:** `FR-A-3.x`
  - Mock 데이터를 기반으로 개발되었던 평가 진행 UI를 실제 백엔드 API와 연동하여 최종 완료했습니다.
  - **주요 구현 내용**:
    - `MyEvaluationsPage`에서 `getUserHistory`, `getMySubordinates`, `getProjectMembers` API를 호출하여 실제 평가 대상자 목록을 동적으로 구성하도록 리팩토링했습니다.
    - 정성평가, PM평가, 동료평가 다이얼로그에 실제 데이터를 전달하여 기능이 완전하게 동작하도록 수정했습니다.
  - 상세 개발 내역은 [../devlog/task_6_4_evaluation_ui.md](../devlog/task_6_4_evaluation_ui.md) 및 [../devlog/task_6_4_evaluation_ui_integration.md](../devlog/task_6_4_evaluation_ui_integration.md) 문서를 참고하세요.

- **Task 6.5: 최종 등급 조정 UI 개발 (완료)**
  - **요구사항:** `FR-A-4.4, 4.5`
  - 실장 및 관리자가 하위 조직원의 최종 등급을 조정할 수 있는 페이지를 구현했습니다.
  - **주요 구현 내용**:
    - 관리자/실장 전용 라우팅 및 네비게이션 메뉴를 추가했습니다.
    - `DataGrid`를 사용하여 하위 조직원의 점수 및 등급 현황을 표시하고, 등급을 직접 수정할 수 있는 UI를 구현했습니다.
    - B+와 B- 등급의 인원수가 동일해야 한다는 비즈니스 규칙을 프론트엔드에서 실시간으로 검증하는 로직을 추가했습니다.
  - 상세 개발 내역은 [../devlog/task_6_5_final_grade_adjustment_ui.md](../devlog/task_6_5_final_grade_adjustment_ui.md) 문서를 참고하세요.

- **Task 6.6: 평가 결과 및 이력 조회 UI 개발 (완료)**
  - **요구사항:** `FR-A-5.x`
  - 사용자가 자신의 과거 평가 결과와 프로젝트 이력을 조회할 수 있는 페이지를 구현했습니다.
  - **주요 구현 내용**:
    - 모든 사용자가 접근할 수 있는 'My History' 페이지를 생성하고 네비게이션을 추가했습니다.
    - Accordion UI를 사용하여 평가 기간별로 결과를 명확하게 구분하여 보여줍니다.
    - 사용자의 역할(일반 사용자 vs 관리자/실장)에 따라 API로부터 받은 데이터의 노출 수준을 프론트엔드에서 제어하여, 민감한 점수 정보가 권한 없는 사용자에게 보이지 않도록 구현했습니다.
  - 상세 개발 내역은 [../devlog/task_6_6_evaluation_history_ui.md](../devlog/task_6_6_evaluation_history_ui.md) 문서를 참고하세요.


