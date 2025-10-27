# Phase 5: 프론트엔드 기반 구축

이 문서는 `WORK_PLAN.md`의 Phase 5에 해당하는 프론트엔드 기반 구축 작업에 대한 상세 내용을 기록합니다.

## 1. 프론트엔드 프로젝트 초기 설정 (Task 5.1)

- **목표**: React, Vite, TypeScript 기반의 프론트엔드 프로젝트를 `frontend` 디렉터리에 초기 설정합니다.
- **수행 내용**:
    - `frontend` 디렉터리 내 기존 파일(placeholder)을 삭제했습니다.
    - `npx create-vite@latest . --template react-ts` 명령을 사용하여 React, TypeScript 프로젝트를 생성했습니다.
    - `package.json`, `tsconfig.json`, `vite.config.ts` 등 기본 설정 파일이 생성되었음을 확인했습니다.

## 2. 인증 UI 및 로직 개발 (Task 5.2)

- **목표**: 사용자 로그인 기능을 위한 UI 및 백엔드 API 연동 로직을 개발합니다.
- **수행 내용**:
    - HTTP 요청을 처리하기 위해 `axios` 라이브러리를 설치했습니다 (`npm install axios`).
    - `src/services/api.ts` 파일을 생성하여 `axios` 인스턴스를 설정하고, JWT 토큰을 요청 헤더에 자동으로 포함시키는 인터셉터를 구현했습니다.
    - `api.ts` 파일에 `login`, `logout`, `getCurrentUser`와 같은 인증 관련 함수를 정의했습니다.
    - `src/pages/Login.tsx` 컴포넌트를 생성하여 사용자 이름과 비밀번호를 입력받는 로그인 폼 UI를 구현했습니다.
    - 로그인 성공 시 `localStorage`에 `access_token`을 저장하고, 실패 시 에러 메시지를 표시하도록 로직을 구현했습니다.

## 3. 공통 레이아웃 및 네비게이션 구현 (Task 5.3)

- **목표**: 애플리케이션 전반에 걸쳐 사용될 공통 레이아웃(헤더, 사이드바, 푸터)과 페이지 간 이동을 위한 네비게이션을 구현합니다.
- **수행 내용**:
    - `react-router-dom` 라이브러리를 설치했습니다 (`npm install react-router-dom`).
    - `src/components/Layout.tsx` 컴포넌트를 생성하여 헤더, 사이드바, 푸터 및 메인 콘텐츠 영역을 포함하는 기본 레이아웃을 정의했습니다.
    - `Layout.tsx` 내에 기본적인 네비게이션 링크(Home, Profile, Evaluations 등)와 로그아웃 버튼을 추가했습니다.
    - `src/App.tsx`를 수정하여 `BrowserRouter`, `Routes`, `Route`를 사용하여 라우팅을 설정하고, 로그인 상태에 따라 `Login` 페이지 또는 `Layout` 컴포넌트가 렌더링되도록 조건부 렌더링을 구현했습니다.

## 4. 대시보드 페이지 구현 (Task 5.4)

- **목표**: 로그인 후 사용자가 처음 보게 될 메인 대시보드 페이지를 구현합니다.
- **수행 내용**:
    - `src/App.tsx` 내에 `Dashboard` 컴포넌트를 정의했습니다.
    - `Dashboard` 컴포넌트에서는 `auth.getCurrentUser()`를 호출하여 현재 로그인한 사용자 정보를 가져와 환영 메시지와 함께 표시하도록 했습니다.
    - 간단한 통계 정보(예: Total Praises Received, Projects Participated)를 포함하는 플레이스홀더 위젯을 추가했습니다.

## 5. 기본 사용자 프로필 페이지 구현 (Task 5.5)

- **목표**: 사용자가 자신의 정보를 확인하고 외부 계정 연동을 관리할 수 있는 프로필 페이지를 구현합니다.
- **수행 내용**:
    - `src/App.tsx` 내에 `Profile` 컴포넌트를 정의했습니다.
    - `Profile` 컴포넌트에서는 `auth.getCurrentUser()`를 호출하여 사용자 이름, 이메일, 전체 이름, 역할, 소속 조직 등의 상세 정보를 표시하도록 했습니다.
    - 외부 계정 연동을 위한 플레이스홀더 섹션을 추가했습니다.

## 결론

Phase 5의 모든 작업이 성공적으로 완료되었습니다. 이제 프론트엔드 애플리케이션은 기본적인 프로젝트 설정, 사용자 인증, 공통 레이아웃 및 네비게이션, 그리고 대시보드 및 프로필 페이지를 갖추게 되었습니다. 다음 단계에서는 각 기능에 대한 UI 개발을 진행할 수 있습니다.
