# 개발 로그: 프로젝트 조회 및 멤버 할당 권한 문제 해결

## 1. 작업 일시
2025-10-29

## 2. 이슈 요약
- **문제:** 실장(Dept Head)이 프로젝트 조회 시, 자신의 하위 조직원이 PM인 프로젝트만 필터링되지 않아 UI에 정상적으로 표시되지 않는 문제가 발생. 프로젝트 멤버 할당 시에도 유사한 권한 문제가 존재. Admin 또한 전역적인 조회/관리가 불가능했음.
- **원인:** `GET /projects/` 및 `POST /projects/{id}/members` API 엔드포인트에 사용자의 역할(Admin, Dept Head)에 따른 데이터 필터링 및 권한 분기 로직이 부재했음.

## 3. 개발 목표
1.  **프로젝트 조회 API 수정:** 사용자의 역할에 따라 조회되는 프로젝트 목록을 필터링한다.
    - **Admin:** 모든 프로젝트 조회
    - **Dept Head:** 자신의 하위 조직원이 PM인 프로젝트만 조회
2.  **프로젝트 멤버 추가 API 수정:** 사용자의 역할에 따라 멤버 추가 권한을 다르게 적용한다.
    - **Admin:** 모든 프로젝트에 모든 사용자 추가 가능
    - **Dept Head:** 자신의 부서 프로젝트에 자신의 부서원만 추가 가능
3.  **사용자 조회 API 수정:** 실장이 프로젝트 멤버로 할당할 하위 조직원을 조회할 수 있도록 권한을 확장한다.
    - **Admin:** 모든 사용자 조회
    - **Dept Head:** 자신의 하위 조직원만 조회

## 4. 변경된 파일 목록
- `app/crud/project.py`
  - `get_multi_for_user` 함수를 추가하여, DB 조회 시 역할 기반 필터링 로직 구현.
- `app/api/endpoints/projects.py`
  - `read_projects`: `get_multi_for_user`를 사용하도록 변경.
  - `add_project_member`: Admin 역할일 경우 부서 제약 조건을 건너뛰도록 로직 수정.
- `app/api/endpoints/users.py`
  - `read_users`: Admin과 Dept Head 역할에 따라 다른 사용자 목록을 반환하도록 수정.
- `app/api/deps.py`
  - `get_current_admin_or_dept_head_user` 의존성을 추가하여 Admin 또는 Dept Head 권한을 확인하는 로직 재사용.
- `docs/api/users/get_users.md` (신규 생성)
  - `GET /users/` API 명세 추가.
- `docs/api/projects/get_projects.md` (신규 생성)
  - `GET /projects/` API 명세 추가.
- `docs/api/projects/add_project_member.md` (수정)
  - Admin의 전역적 멤버 추가 권한에 대한 설명 보강.

## 5. 결론
CRUD, API, 의존성 주입 계층을 모두 수정하여 역할 기반 권한 모델을 명확히 적용함. 또한, 변경 사항에 맞춰 API 문서를 생성 및 수정하여 최신 상태를 유지함.
