# 프로젝트 현재 상태 요약

이 문서는 'Growth-Wave: 듀얼 트랙 인사 플랫폼' 프로젝트의 현재 진행 상황과 주요 성과를 요약합니다.

## 1. 프로젝트 개요 및 진행 현황

'Growth-Wave' 프로젝트는 공정한 평가(Track A)와 구성원의 성장 및 인정(Track B)이라는 두 가지 핵심 목표를 동시에 달성하기 위해 진행되고 있습니다. 현재 백엔드 시스템의 핵심 기반 구축 및 Track A의 주요 기능 개발을 완료했으며, Track B 기능 개발을 진행 중입니다.

## 2. 주요 성과

### Phase 1: FastAPI 기본 설정 및 사용자 인증 구현 (완료)

*   **핵심 기반 구축:** FastAPI 기반의 프로젝트 구조를 확립하고, SQLAlchemy 모델 및 Pydantic 스키마를 정의하여 데이터 관리의 기반을 마련했습니다.
*   **보안 및 인증:** `.env`를 통한 설정 관리, `passlib`을 이용한 비밀번호 암호화, JWT 기반의 사용자 인증 시스템(`app/core/security.py`, `app/api/endpoints/auth.py`)을 성공적으로 구현했습니다.
*   **기본 관리 기능:** 사용자 및 조직 생성/조회 API(`app/api/endpoints/users.py`, `app/api/endpoints/organizations.py`)를 개발하여 시스템의 기본 운영 기능을 확보했습니다.
*   **테스트 환경:** `pytest` 기반의 테스트 환경을 구축하고 초기 API에 대한 테스트 코드를 작성하여 개발 안정성을 높였습니다.

### Phase 2: Track A - 평가 설정 핵심 기능 개발 (완료)

*   **조직도 관리:** 관리자가 조직도 파일을 업로드하여 조직 구조를 일괄 동기화하는 기능(`POST /api/v1/organizations/upload`)을 구현했습니다.
*   **프로젝트 참여 비중 설정:** 실장이 소속 인원의 프로젝트별 참여 비중을 설정할 수 있는 API(`POST /api/v1/projects/members/weights`)를 개발했습니다.
*   **평가 항목 가중치 설정:** 관리자가 직책별 평가 항목의 가중치를 설정하는 API(`/api/v1/evaluations/`)를 구현했습니다.
*   **PM동료평가:** 동료에게 점수를 부여하는 API(`POST /api/v1/evaluations/peer-evaluations/`)를 개발했으며, 평균 점수 제한 등 어뷰징 방지 로직을 포함합니다.
*   **프로젝트 멤버 및 하위 조직원 조회 API:** 프론트엔드(Phase 6.4)에서 평가 대상자 선택 화면 구현에 필요한 프로젝트 멤버 조회 API (`GET /api/v1/projects/{project_id}/members`)와 관리자의 하위 조직원 조회 API (`GET /api/v1/users/me/subordinates`)를 구현했습니다.
*   **안정화:** 개발 과정에서 발생한 다수의 테스트 실패를 성공적으로 해결하여 기능의 안정성을 확보했으며, 모든 테스트가 통과함을 확인했습니다.

### Phase 3: Track B 기능 개발 (진행 중)

*   **외부 계정 연동:** Jira, Bitbucket 등 외부 계정을 시스템에 안전하게 연동하는 기능이 개발 완료되었습니다. (상세 내용은 `docs/devlog/task_3_1_external_account_integration.md` 참조)
*   **칭찬 인박스 & 강점 프로필:** 익명 칭찬 전송, 개인 칭찬 인박스, 공개 강점 프로필 기능이 개발 완료되었습니다. 칭찬 횟수 제한을 통한 어뷰징 방지 로직도 포함되어 있습니다. (상세 내용은 `docs/devlog/task_3_5_3_6_praise_inbox_strength_profile.md` 참조)

## 3. 다음 단계

`WORK_PLAN.md`에 따라, 다음 주요 작업은 **Task 3.2: AI 회고록 생성 API 개발**입니다. 사용자의 연동된 외부 계정 활동 내역을 기반으로 LLM을 활용하여 회고록 초안을 생성하는 기능을 구현할 예정입니다.
