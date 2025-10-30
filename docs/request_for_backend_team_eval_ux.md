# 백엔드 팀 요청사항: 평가 결과 조회 UX 개선을 위한 API 개발

안녕하세요. 프론트엔드 팀입니다.

현재 '평가 결과 및 이력 조회' 페이지의 사용자 경험(UX)을 개선하는 작업을 진행하고 있습니다.
기존의 Accordion 방식에서 벗어나, 아래와 같은 새로운 워크플로우를 도입하고자 합니다.

1.  사용자(관리자/실장)가 먼저 **평가 기간**을 선택합니다.
2.  선택된 기간에 평가가 완료된 **인원 목록**이 표시됩니다.
3.  특정 인원을 선택하면, 해당 인원의 **상세 평가 내역**이 표시됩니다.

이 새로운 UX를 구현하기 위해 백엔드에 다음과 같은 신규 API 2종의 개발을 요청드립니다.

### 신규 API 목록

1.  `GET /api/v1/evaluations/periods/{period_id}/evaluated-users`
2.  `GET /api/v1/evaluations/periods/{period_id}/users/{user_id}/details`

### 상세 명세

자세한 API 요청/응답 형식 및 권한 등은 아래의 신규 API 명세 문서를 참고해 주시기 바랍니다.

-   [./api/evaluations/get_evaluated_users_by_period.md](./api/evaluations/get_evaluated_users_by_period.md)
-   [./api/evaluations/get_detailed_evaluation_result.md](./api/evaluations/get_detailed_evaluation_result.md)

### 핵심 구현 요청 사항

-   **상세 결과 API (`.../details`)**: 해당 API는 `FinalEvaluation`, `ProjectMember`, `PeerEvaluation`, `PmEvaluation`, `QualitativeEvaluation` 등 여러 테이블의 데이터를 조합하여 응답을 구성해야 합니다.
-   **평가 미완료 처리**: 상세 결과 조회 시, 최종 평가가 아직 완료되지 않은 사용자에 대해서는 404 Not Found 오류 대신, 명세에 정의된 대로 `status: "IN_PROGRESS"` 와 함께 200 OK 응답을 보내주셔야 프론트엔드에서 "아직 평가가 완료되지 않았습니다"와 같은 안내 문구를 정상적으로 표시할 수 있습니다.
-   **접근 권한**: 두 API 모두 `DEPT_HEAD`와 `ADMIN` 역할에 대한 엄격한 접근 제어 로직(하위 조직원 여부 등)이 필요합니다.

---

위 API 개발이 완료되면 프론트엔드에서 새로운 평가 결과 조회 화면을 구현할 예정입니다.

협조에 감사드립니다.
