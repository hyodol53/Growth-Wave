# Phase 3: Track B 기능 개발 (진행 중)

`WORK_PLAN.md`의 Phase 3 목표에 따라 Track B 기능 개발을 진행하고 있습니다.

---

## 완료된 작업

- **Task 3.1: 외부 계정(Jira, Bitbucket) 연동 기능 개발** `(완료)`
  - 상세 개발 내역은 [../devlog/task_3_1_external_account_integration.md](../devlog/task_3_1_external_account_integration.md) 문서를 참고하세요.

- **Task 3.5 & 3.6: 칭찬 인박스 & 강점 프로필 기능 개발** `(완료)`
  - 상세 개발 내역은 [../devlog/task_3_5_3_6_praise_inbox_strength_profile.md](../devlog/task_3_5_3_6_praise_inbox_strength_profile.md) 문서를 참고하세요.

- **Task 3.7: 익명 칭찬 이름 생성 로직 개선** `(완료)`
  - 발신자와 수신자 쌍에 대해 일관된 익명 이름(색상+동물)을 생성하도록 로직을 개선했습니다. 상세 내역은 [../devlog/task_3_7_anonymous_praise_names.md](../devlog/task_3_7_anonymous_praise_names.md) 문서를 참고하세요.

- **Task 3.2: AI 회고록 생성 API 개발** `(완료)`
  - 외부 계정 활동을 기반으로 LLM을 통해 비공개 회고록 초안을 생성하는 API를 개발했습니다. 상세 내역은 [../devlog/task_3_2_ai_retrospective_api.md](../devlog/task_3_2_ai_retrospective_api.md) 문서를 참고하세요.

- **Task 3.3: 협업 네트워크 데이터 수집기 개발** `(완료)`
  - 외부 시스템의 활동을 분석하여 사용자 간의 상호작용 관계 데이터를 수집하는 기능을 개발했습니다. 상세 내역은 [../devlog/task_3_3_collaboration_network_collector.md](../devlog/task_3_3_collaboration_network_collector.md) 문서를 참고하세요.

- **Task 3.4: 협업 네트워크 시각화 API 개발** `(완료)`
  - 수집된 협업 데이터를 기반으로 조직/프로젝트별 협업 관계도 및 분석 데이터를 제공하는 API를 개발했습니다. 상세 내역은 [../devlog/task_3_4_collaboration_network_visualization.md](../devlog/task_3_4_collaboration_network_visualization.md) 문서를 참고하세요.

---

## 다음 단계 (Next Steps)

`WORK_PLAN.md`에 따라, 다음 작업으로 **Task 3.4: 협업 네트워크 시각화 API 개발**을 진행할 예정입니다.

- **요구사항**: `FR-B-2.2`, `FR-B-2.3`
- **목표**: 수집된 협업 데이터를 기반으로 조직/프로젝트별 협업 관계도 및 분석 데이터를 제공하는 API를 개발합니다.