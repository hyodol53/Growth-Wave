# 평가 페이지 UX 개선 및 API 구현 요청

## 1. 프론트엔드 UX 개선 요구사항

사용자 경험(UX) 향상을 위해 '내 평가' 페이지를 다음과 같이 개선하고자 합니다.

1.  **평가 영역 분리:**
    *   '정성평가'는 팀장/부서장 등 특정 보직자에게만 해당되므로, 일반적인 '프로젝트 평가'(동료평가, PM평가)와 시각적으로 명확히 구분되는 영역으로 분리합니다.

2.  **프로젝트 기반 평가 UI 도입:**
    *   **프로젝트 선택 기능:** 현재 평가해야 할 프로젝트 목록을 드롭다운(콤보박스) 형태로 제공하여 사용자가 평가할 프로젝트를 직접 선택하게 합니다.
    *   **그리드(Grid) 기반 평가:** 프로젝트를 선택하면, 해당 프로젝트의 평가 대상자들이 테이블(표) 형태의 그리드로 표시됩니다. 각 행(row)에는 점수 입력란과 서술형 피드백 입력란이 포함됩니다.
    *   **역할에 따른 그리드 표시:** 사용자가 선택한 프로젝트에서 PM 역할이면 'PM 평가' 그리드를, 일반 구성원 역할이면 '동료평가' 그리드를 표시합니다.

3.  **평가 수정 및 제출 UX 변경:**
    *   **상시 수정 기능:** 평가 기간 동안에는 사용자가 제출한 평가를 언제든지 다시 조회하고 수정할 수 있어야 합니다.
    *   **프로젝트별 제출:** 평가는 프로젝트 단위로 각각 제출할 수 있습니다.
    *   **통합 페이지:** '평가 시작하기'와 같은 별도 단계 없이, 한 페이지 내에서 평가 현황 조회, 평가 진행, 수정, 제출이 모두 가능하도록 구성합니다.

## 2. 백엔드 API 구현 및 수정 요청사항

위 UX를 구현하기 위해 다음 API들의 신규 개발 및 수정이 필요합니다.

### 2.1. 신규 API

#### 1. `GET /api/v1/evaluations/my-tasks`
- **설명:** 현재 로그인한 사용자가 **이번 평가 기간에 평가해야 할 모든 프로젝트 목록**을 조회하는 API입니다.
- **필요성:** 평가 페이지의 프로젝트 선택 드롭다운 메뉴를 구성하기 위해 필수적입니다.
- **응답 데이터 예시:**
  ```json
  [
    {
      "project_id": 1,
      "project_name": "Growth-Wave 개발",
      "user_role_in_project": "PM" 
    },
    {
      "project_id": 2,
      "project_name": "신규 서비스 기획",
      "user_role_in_project": "MEMBER"
    }
  ]
  ```

#### 2. `GET /api/v1/evaluations/peer-evaluations/{project_id}`
- **설명:** 특정 프로젝트(`project_id`)에 대해, 현재 로그인한 사용자가 **이미 평가했거나 평가해야 할 동료 목록과 기존 평가 내용(점수, 코멘트)**을 조회하는 API입니다.
- **필요성:** 프로젝트 선택 시, 동료 평가 그리드에 기존에 저장된 내용을 채우기 위해 필요합니다.
- **응답 데이터 예시:**
  ```json
  {
    "project_id": 1,
    "project_name": "Growth-Wave 개발",
    "status": "IN_PROGRESS", 
    "peers_to_evaluate": [
      {
        "evaluatee_id": 10,
        "evaluatee_name": "김동료",
        "score": 85, 
        "comment": "항상 적극적으로 도와주셔서 감사합니다." 
      },
      {
        "evaluatee_id": 12,
        "evaluatee_name": "박동료",
        "score": null,
        "comment": null
      }
    ]
  }
  ```

### 2.2. 기존 API 수정

#### 1. `POST /api/v1/evaluations/peer-evaluations/`
- **수정 사항:**
    1.  **서술형 피드백(`comment`) 필드 추가:** 요청 Body에 `comment` (string, optional) 필드를 추가합니다.
    2.  **생성 및 수정(UPSERT) 기능:** 동일 평가 건에 대해 데이터가 이미 존재하면 새로 생성하는 대신 기존 데이터를 덮어쓰도록(UPDATE) 로직을 수정합니다.
- **수정된 요청 Body 예시:**
  ```json
  {
    "project_id": 1,
    "evaluations": [
      {
        "evaluatee_id": 2,
        "score": 65,
        "comment": "피드백 내용입니다."
      },
      {
        "evaluatee_id": 3,
        "score": 70,
        "comment": "수정된 피드백입니다."
      }
    ]
  }
  ```

#### 2. `POST /api/v1/evaluations/pm-evaluations/`
- **수정 사항:** `peer-evaluations`와 동일하게 **`comment` 필드 추가** 및 **생성/수정(UPSERT) 기능**이 필요합니다.

## 3. 프론트엔드 구현 내용

요청된 UX 개선 사항과 API 명세에 맞춰 프론트엔드 구현을 완료했습니다.

1.  **`MyEvaluationsPage.tsx` 리팩토링:**
    -   기존의 다이얼로그 기반 평가 로직을 모두 제거하고, 페이지 내에서 모든 평가가 이루어지도록 구조를 변경했습니다.
    -   정성평가(`QualitativeEvaluationCard`)와 프로젝트 평가 영역을 시각적으로 분리했습니다.
    -   `useEffect` 훅에서 `getMyTasks` API를 호출하여 평가할 프로젝트 목록을 가져와 드롭다운 메뉴를 동적으로 생성합니다.
    -   프로젝트 선택 시(`handleProjectChange`), 사용자의 역할에 따라 `getPeerEvaluations` 또는 `getPmEvaluations` API를 호출하여 해당 프로젝트의 평가 데이터를 비동기적으로 불러옵니다.

2.  **신규 컴포넌트 생성 및 구현:**
    -   `PeerEvaluationGrid.tsx` 및 `PmEvaluationGrid.tsx`:
        -   API로부터 받은 평가 데이터를 props로 받아 Material-UI의 `Table` 컴포넌트를 사용해 평가 그리드를 렌더링합니다.
        -   사용자가 입력하는 점수와 코멘트는 내부 `useState`로 관리됩니다.
        -   `onSubmit` prop으로 받은 함수를 통해, 사용자가 입력한 평가 데이터를 부모 컴포넌트(`MyEvaluationsPage`)로 전달하여 최종 제출합니다.

3.  **UX 개선 사항 반영:**
    -   평가 데이터의 `status` 값('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED')을 확인합니다.
    -   `status` 값에 따라 제출 버튼의 텍스트를 '제출' 또는 '수정 제출'로 동적으로 변경하여, 사용자에게 현재 상태를 명확하게 인지시킵니다.

## 3. 완료된 작업 내역 (백엔드)

- **신규 API 3종 개발 완료**
  - `GET /api/v1/evaluations/my-tasks`
  - `GET /api/v1/evaluations/peer-evaluations/{project_id}`
  - `GET /api/v1/evaluations/pm-evaluations/{project_id}`
- **기존 API 2종 수정 완료**
  - `POST /api/v1/evaluations/peer-evaluations/`: `comment` 필드 추가 및 UPSERT 기능 구현
  - `POST /api/v1/evaluations/pm-evaluations/`: `comment` 필드 추가 및 UPSERT 기능 구현
- **단위 테스트 및 리그레션 테스트**
  - 신규/수정된 API에 대한 단위 테스트 코드(`tests/api/test_evaluations_ux.py`) 작성 완료
  - 전체 테스트 스위트(`pytest`) 실행하여 모든 테스트 통과 확인 (123개 통과)
- **API 문서화 완료**
  - `docs/api/evaluations/` 경로에 관련 API 명세서 4건 추가/수정 완료
