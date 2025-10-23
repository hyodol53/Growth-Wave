# Task 2.7: Growth & Culture 리포트 조회 API 개발 (FR-A-4.6)

`REQUIREMENTS.md`의 `FR-A-4.6` 요구사항에 따라, 관리자가 특정 직원의 'Growth & Culture 리포트'를 조회할 수 있는 API를 개발했습니다. 이 기능은 평가 과정에서 관리자의 주관적 판단을 돕는 참고 자료를 제공하는 핵심적인 역할을 합니다.

## 1. 핵심 기능

- **리포트 조회 API:** `GET /api/v1/users/{user_id}/growth-culture-report` 엔드포인트를 통해 특정 사용자의 리포트를 조회합니다.
- **강점 프로필 제공:** 리포트의 일부로, 기존에 구현된 '칭찬하기' 기능에서 집계된 데이터 기반의 '강점 프로필'(`StrengthProfile`)을 포함하여 반환합니다.
- **권한 제어:** `ADMIN` 또는 `DEPT_HEAD` 역할만 API에 접근할 수 있습니다. 특히 `DEPT_HEAD`는 자신이 속한 조직 및 모든 하위 조직의 구성원에 대해서만 조회가 가능하도록 엄격한 권한 검사를 구현했습니다.

## 2. 기술적 구현 세부 사항

- **API 스키마 (`app/schemas/report.py`):**
    - 리포트 응답을 위한 `GrowthAndCultureReport` Pydantic 스키마를 새로 정의했습니다.
    - 기존 `StrengthProfile` 스키마에 누적 칭찬 횟수를 나타내는 `total_praises` 필드를 추가하여 데이터의 효용성을 높였습니다.

- **API 엔드포인트 (`app/api/endpoints/reports.py`):**
    - `/api/v1` 아래에 `reports` 라우터를 신설하고 리포트 조회 엔드포인트를 구현했습니다.
    - `DEPT_HEAD`의 하위 조직원 여부를 판단하기 위해 `crud.organization.get_all_descendant_orgs` 함수를 사용하여 허용된 조직 ID 목록을 구성하고, 이를 통해 접근 권한을 확인하는 로직을 구현했습니다.

- **테스트 및 안정화 (`tests/api/test_reports.py`):**
    - 기능의 정상 동작(실장, 관리자) 및 비정상 케이스(권한 없는 직원, 다른 부서 실장)에 대한 테스트 케이스를 작성하여 기능의 안정성과 보안을 검증했습니다.
    - 테스트 과정에서 `AttributeError` (잘못된 CRUD 함수 호출), `KeyError` (스키마와 테스트 간의 필드 불일치) 등 다양한 오류를 발견하고 수정했습니다.
    - 특히 `total_praises` 필드의 집계 방식이 '총 칭찬 수'가 아닌 '총 해시태그 수'로 잘못 계산되던 논리적 오류를 바로잡아 정확한 데이터를 반환하도록 수정했습니다.

## 3. 결론

'Growth & Culture 리포트 조회' 기능의 백엔드 구현이 안정적으로 완료되었으며, 모든 테스트가 통과함을 확인했습니다. 이로써 Track A와 Track B를 연결하는 중요한 기능적 요구사항이 충족되었습니다.
