# Growth-Wave 기술 아키텍처 설계 (v0.1)

## 1. 개요
이 문서는 'Growth-Wave: 듀얼 트랙 인사 플랫폼'의 기술적인 설계와 아키텍처를 정의합니다. 다른 AI 에이전트 또는 개발자가 프로젝트의 구조를 이해하고 협업하는 것을 돕기 위한 기술 지침서 역할을 합니다.

## 2. 기술 스택 (Technology Stack)
- **Backend:** Python 3.9+, FastAPI
- **Database:** SQLite (개발용), SQLAlchemy (ORM)
- **API Schema & Validation:** Pydantic
- **Authentication:** JWT (JSON Web Tokens) 기반, Passlib (비밀번호 해싱)
- **Web Server:** Uvicorn (ASGI)
- **Future Frontend (TBD):** React 또는 Vue.js 와 같은 모던 JavaScript 프레임워크 사용을 권장

## 3. 시스템 아키텍처
### 3.1. 아키텍처 스타일
- **분리된 백엔드/프론트엔드:** 백엔드는 RESTful API 서버의 역할을 수행하고, 프론트엔드는 이 API를 호출하여 UI를 렌더링하는 방식으로 구성합니다.
- **모놀리식 API 백엔드:** 백엔드 애플리케이션은 단일 FastAPI 프로젝트로 구성됩니다. 하지만 내부적으로는 기능(평가, 성장, 사용자 등)에 따라 라우터(Router)와 모듈을 분리하여 논리적인 모듈화를 추구합니다.

### 3.2. 핵심 원칙: 조건부 데이터 참조
- `Track A (평가)`와 `Track B (성장)`는 논리적으로 분리된 모듈로 개발됩니다.
- 두 트랙 간의 데이터 참조는 `system_info.md`에 명시된 'Growth & Culture 리포트'를 통해서만 제한적으로 이루어지며, 이는 API 레벨에서 제어됩니다.

## 4. 프로젝트 구조 (디렉터리 레이아웃)
```
D:\test_gemini\해커톤\
├── app/                  # FastAPI 애플리케이션 소스 코드
│   ├── api/              # API 엔드포인트 (라우터)
│   ├── core/             # 핵심 로직 (DB 연결, 설정, 보안 등)
│   ├── models/           # SQLAlchemy DB 모델
│   ├── schemas/          # Pydantic 데이터 스키마
│   ├── crud/             # (생성 예정) DB CRUD(Create, Read, Update, Delete) 함수
│   └── main.py           # FastAPI 앱 메인 진입점
├── tests/                # (생성 예정) 테스트 코드
├── ARCHITECTURE.md       # 본 문서
├── requirement.md        # 요구사항 명세서
├── requirements.txt      # Python 패키지 의존성
└── system_info.md        # 시스템 개요서
```

## 5. 핵심 데이터 모델
`app/models/` 디렉터리에 SQLAlchemy 모델로 정의됩니다.
- **`user.py` (User 모델):**
    - `id`, `username`, `email`, `hashed_password`, `full_name` 등 사용자 기본 정보
    - `role`: 사용자의 역할을 정의하는 Enum (`employee`, `team_lead`, `dept_head`, `admin`)
    - `organization_id`: 사용자가 속한 조직(부서)와의 관계 (Foreign Key)
- **`organization.py` (Organization 모델):**
    - `id`, `name`, `level` (1: 센터, 2: 실, 3: 팀) 등 조직 정보
    - `parent_id`: 상위 조직과의 관계를 나타내는 자기 참조(self-referential) 관계

## 6. API 설계 원칙
- **RESTful:** 모든 리소스는 명사 형태의 URL로 표현하고, HTTP 동사(GET, POST, PUT, DELETE)를 사용하여 상태를 변경합니다.
- **Versioning:** API URL에 버전 정보를 포함합니다. (예: `/api/v1/...`)
- **Schema-driven:** 모든 요청(Request)과 응답(Response)은 Pydantic 스키마를 사용하여 명확하게 정의하고 유효성을 검사합니다.

## 7. 인증 및 권한 부여 (Authentication & Authorization)
- **인증 (Authentication):**
    - 사용자가 ID/PW로 `/api/v1/auth/token` 엔드포인트에 요청하면, 서버는 유효성을 검증한 후 JWT Access Token을 발급합니다.
    - 이후 모든 API 요청 시, 클라이언트는 HTTP Header에 `Authorization: Bearer <token>` 형태로 토큰을 포함하여 전송해야 합니다.
- **권한 부여 (Authorization):**
    - 역할 기반 접근 제어(RBAC)를 사용합니다.
    - 각 API 엔드포인트는 FastAPI의 의존성 주입(Dependency Injection) 시스템을 사용하여 필요한 사용자 역할(`UserRole`)을 확인하고, 권한이 없는 경우 접근을 차단합니다.

## 8. 설정 관리 (Configuration Management)
- `requirement.md`에서 정의된 설정값들(AI 모델 종류, 칭찬 횟수 제한 등)은 관리자가 UI를 통해 변경할 수 있도록 별도의 API와 DB 모델을 설계합니다.
- 초기 기본값 및 DB 연결 정보 등 민감한 정보는 `.env` 파일과 Pydantic의 `BaseSettings`를 사용하여 관리하는 것을 권장합니다. (추후 `app/core/config.py` 파일 생성 예정)
