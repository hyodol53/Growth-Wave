# '칭찬 인박스' & '강점 프로필' (FR-B-3) 설계 명세서 (v2: 카테고리 선택)

## 1. 설계 목표
'칭찬 인박스' 및 '강점 프로필' 기능의 설계를 정의한다.
본 설계의 핵심 목표는 다음과 같다:
1.  **데이터의 철저한 분리**: 칭찬 메시지 원문(Private)과 강점 뱃지(Public) 데이터를 분리하여 관리자조차 사적인 메시지를 열람할 수 없도록 보장한다.
2.  **신뢰할 수 있는 익명성**: 칭찬 발신자는 '익명의 동물'로 표시되어 수신자에게 긍정적인 피드백을 부담 없이 전달할 수 있게 한다.
3.  **어뷰징 방지**: 특정인에게 칭찬이 편중되는 것을 막기 위해, 평가 주기별 칭찬 횟수를 제한하는 로직을 구현한다.
4.  **(수정) 데이터 집계(Clustering) 보장**: 사용자가 해시태그를 직접 입력하는 대신, **사전에 정의된 '강점 카테고리'를 선택**하게 하여 '강점 프로필' 데이터의 정합성을 확보한다.

---

## 2. 핵심 설계 결정: '익명성' vs '어뷰징 방지'

요구사항 `NFR-5`는 관리자조차 발신자를 식별할 수 없도록 '발신자 정보 비저장'을 권장하지만, `FR-B-3.6`은 '특정 사용자에게 보낼 수 있는 칭찬 횟수'를 제한해야 하므로, 시스템은 `(발신자, 수신자, 평가주기)`를 알아야만 합니다.

* **설계 결정:** **`FR-B-3.6` (기능 요구사항)을 우선**합니다.
* **구현 방안:**
    1.  데이터베이스(`Praise` 테이블)에는 `sender_id` (발신자)를 **저장합니다.** 이는 횟수 제한 로직(`FR-B-3.6`)을 구현하기 위한 필수 조건입니다.
    2.  `NFR-5`의 '관리자 식별 불가' 목표는 **API 레벨에서 보장**합니다. `sender_id` 컬럼은 그 어떤 API 응답(관리자 API 포함)에도 절대 포함되지 않으며, 오직 `POST /praise` 요청 시 서버 내부의 횟수 제한 로직에서만 사용됩니다.

---

## 3. 데이터 모델 (Database Schema)

### 3.1. `Praise` (칭찬 원본 데이터)
* **설명**: 칭찬이 발생할 때마다 저장되는 원본 데이터 (로우 데이터).
* **접근 제어**: **시스템 내부용 (Strictly Private)**. 오직 수신자 본인만 `GET /inbox` API를 통해 `message`와 `hashtag`를 조회할 수 있습니다. `sender_id`는 절대 외부에 노출되지 않습니다.

| 컬럼명 | 데이터 타입 | 설명 | 비고 |
| :--- | :--- | :--- | :--- |
| `praise_id` | `BIGINT` (PK) | 칭찬 고유 ID | |
| `sender_id` | `BIGINT` (FK, User) | **[Private]** 발신자 ID | `FR-B-3.6` 횟수 제한 로직 전용 |
| `receiver_id` | `BIGINT` (FK, User) | **[Private]** 수신자 ID | |
| `message` | `TEXT` | **[Private]** 칭찬 메시지 원문 | `FR-B-3.2` (수신자만 열람) |
| `hashtag` | `VARCHAR(100)` | **(수정) 선택된 강점 카테고리** | (예: "#해결사") |
| `evaluation_period_id` | `BIGINT` (FK) | 평가 주기 ID | `FR-B-3.6` (주기당 횟수 제한) |
| `created_at` | `DATETIME` | 생성 일시 | |

### 3.2. `StrengthProfile` (강점 프로필 집계)
* **설명**: `Praise` 데이터가 저장될 때마다, 이 테이블의 `count`가 1씩 증가 (Upsert)하는 집계용 테이블.
* **접근 제어**: **전체 공개용 (Public)**. 모든 사용자가 타인의 프로필을 조회할 수 있으며, 관리자 리포트(`FR-B-3.5`)에서도 이 데이터를 사용합니다.

| 컬럼명 | 데이터 타입 | 설명 | 비고 |
| :--- | :--- | :--- | :--- |
| `user_id` | `BIGINT` (PK, FK) | 사용자 ID (프로필 주인) | |
| `hashtag` | `VARCHAR(100)` (PK) | **(수정) 강점 카테고리** | |
| `evaluation_period_id` | `BIGINT` (PK, FK) | 평가 주기 ID | |
| `count` | `INT` | 누적 횟수 | `FR-B-3.3` (뱃지 집계) |

### 3.3. `SystemConfig` (시스템 설정)
* **설명**: 관리자가 조정 가능한 정책 값을 저장합니다.
* **접근 제어**: 관리자 전용 (Admin)

| 설정 키 (Key) | 값 (Value) | 설명 | 비고 |
| :--- | :--- | :--- | :--- |
| `praise.limit_per_period` | `5` (숫자) | 평가 주기당 동일인에게 보낼 수 있는 최대 칭찬 횟수 | `FR-B-3.6`, `NFR-6` |
| **(수정)** `praise.available_hashtags` | `["#해결사", "#소통왕", "#협업왕", "#선한영향력", "#빠른실행력", "#디테일장인"]` | **(수정) 선택 가능한 강점 카테고리 목록 (Fixed List)** | |
| `praise.anonymous_animals` | `["고라니", "돌고래", ...]` (JSON/String) | '익명의 동물' 목록 | `FR-B-3.1` |

---

## 4. API 설계 (주요 엔드포인트)

### 4.1. `POST /api/v1/praise` (칭찬 전송)
* **인증**: 필수 (로그인한 사용자)
* **Request Body**:
    ```json
    {
      "receiver_id": 123,
      "message": "오늘 발표 정말 인상적이었습니다!",
      "hashtag": "#소통왕" 
    }
    ```
* **핵심 로직 (트랜잭션 처리)**:
    1.  Request Body에서 `receiver_id`, `message`, `hashtag` 추출.
    2.  인증 토큰에서 `sender_id` 추출.
    3.  `SystemConfig`에서 `praise.limit_per_period` (예: 5회) 및 `praise.available_hashtags` (카테고리 목록) 조회.
    4.  현재 활성 `evaluation_period_id` 조회.
    5.  **(추가) 유효성 검사 1**: `hashtag` 값이 `available_hashtags` 목록에 포함되어 있는지 확인. 없으면 `400 Bad Request` (유효하지 않은 해시태그) 반환.
    6.  **유효성 검사 2 (어뷰징 방지 `FR-B-3.6`)**:
        `SELECT COUNT(*) FROM Praise WHERE sender_id = ? AND receiver_id = ? AND evaluation_period_id = ?`
    7.  만약 `COUNT >= 5` 이면, `400 Bad Request` (횟수 초과) 에러 반환.
    8.  `Praise` 테이블에 신규 레코드 삽입 (발신자 ID 포함).
    9.  `StrengthProfile` 테이블에 `(user_id=123, hashtag="#소통왕", period_id=?)`의 `count`를 +1 (Upsert).
    10. `201 Created` 반환.

### 4.2. `GET /api/v1/praise/inbox` (내 칭찬 인박스 조회)
* (변경 사항 없음)
* **인증**: 필수 (로그인한 사용자)
* **핵심 로직 (`FR-B-3.2`)**:
    1.  인증 토큰에서 `receiver_id` 추출.
    2.  `SELECT praise_id, message, hashtag, created_at FROM Praise WHERE receiver_id = ? ORDER BY created_at DESC`
    3.  **'익명의 동물' 생성 (`FR-B-3.1`)**: 조회된 `praise_id`와 `SystemConfig`의 `anonymous_animals` 목록을 조합하여 (예: `animals[praise_id % animals.length]`) '익명의 OOO' 문자열을 동적으로 생성.
* **Response Body**:
    ```json
    [
      {
        "sender_display_name": "익명의 고라니", // DB에 저장된 값이 아님
        "message": "오늘 발표 정말 인상적이었습니다!",
        "hashtag": "#소통왕",
        "received_at": "..."
      },
      ...
    ]
    ```

### 4.3. `GET /api/v1/users/{user_id}/strength-profile` (강점 프로필 조회)
* (변경 사항 없음)
* **인증**: 선택 (모든 사용자가 열람 가능)
* **핵심 로직 (`FR-B-3.3`, `FR-B-3.5`)**:
    1.  Path Parameter에서 `user_id` 추출.
    2.  `SELECT hashtag, count FROM StrengthProfile WHERE user_id = ?` (필요시 `evaluation_period_id`로 필터링)
* **Response Body**:
    ```json
    {
      "user_id": 123,
      "current_period": "2025년 하반기",
      "badges": [
        { "hashtag": "#해결사", "count": 8 },
        { "hashtag": "#소통왕", "count": 5 }
      ]
    }
    ```
* **참고**: 관리자용 'Growth & Culture 리포트'(`FR-A-4.6`)는 이 공개용 API를 사용하여 데이터를 조회합니다.