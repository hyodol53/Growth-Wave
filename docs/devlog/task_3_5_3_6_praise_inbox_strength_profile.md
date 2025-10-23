# Task 3.5 & 3.6: 칭찬 인박스 및 강점 프로필 기능 개발

`WORK_PLAN.md`의 **Task 3.5**와 **Task 3.6**에 해당하는 '칭찬 인박스' 및 '강점 프로필' 기능 개발을 완료했습니다.

- **요구사항 충돌 해결**: 익명성을 보장하면서도 특정인에 대한 칭찬 횟수를 제한해야 하는 상충되는 요구사항(`NFR-5` vs `FR-B-3.6`)을 해결하기 위해, 칭찬 내용 자체는 익명으로 저장하되, 횟수 제한 로직만을 위한 별도의 내부 추적 테이블(`PraiseLimiter`)을 두는 방식으로 아키텍처를 설계하여 두 요구사항을 모두 충족시켰습니다.

- **데이터베이스 모델 (`app/models/`)**:
    - `praise.py`: 발신자 정보를 제외한 칭찬 메시지 모델(`Praise`)을 정의했습니다.
    - `strength.py`: 강점 해시태그(`Strength`)와 칭찬-강점 간의 다대다(N:M) 관계를 정의했습니다.
    - `praise_limiter.py`: 어뷰징 방지를 위해 사용자 간 칭찬 횟수를 기록하는 내부 모델(`PraiseLimiter`)을 정의했습니다.
    - `user.py`: 새로운 모델들과의 관계(Relationship)를 추가했습니다.

- **API 스키마 (`app/schemas/`)**:
    - `praise.py`: 칭찬 생성(`PraiseCreate`) 및 조회(`Praise`)에 사용될 Pydantic 스키마를 정의했습니다.
    - `strength.py`: 사용자의 공개 강점 프로필(`StrengthProfile`) 및 통계(`StrengthStat`) 스키마를 정의했습니다.

- **CRUD 로직 (`app/crud/`)**:
    - `praise.py`: 칭찬 횟수 제한 검사, 칭찬 생성, 칭찬 인박스 조회, 강점 프로필 집계 등 핵심 비즈니스 로직을 구현했습니다.
    - `strength.py`: 해시태그 문자열을 기반으로 강점 데이터를 가져오거나 생성하는 로직을 구현했습니다.

- **API 엔드포인트 (`app/api/endpoints/praises.py`)**:
    - `/api/v1/praises/` 경로에 다음 API를 구현했습니다.
        - `POST /`: 다른 사용자에게 칭찬 메시지와 강점 해시태그를 전송합니다.
        - `GET /inbox/`: 자신의 칭찬 수신함을 조회합니다.
        - `GET /users/{user_id}/strength-profile/`: 특정 사용자의 공개 강점 프로필을 조회합니다.

- **테스트 및 안정화**:
    - 기능의 정상 동작, 권한 처리, 어뷰징 방지 로직을 검증하는 `pytest` 테스트 코드를 작성했습니다.
    - 테스트 과정에서 발견된 `AttributeError`, 정렬 순서 오류, `ValidationError` 등의 문제를 해결하여 모든 테스트가 통과함을 확인하고 기능 안정성을 확보했습니다.