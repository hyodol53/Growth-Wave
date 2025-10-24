# Generate AI Retrospective

## `POST /api/v1/retrospectives/generate`

### 설명
현재 로그인한 사용자의 외부 연동 계정(Jira, Bitbucket 등) 활동 내역을 기반으로, 지정된 기간에 대한 AI 회고록 초안을 생성합니다.

**중요**: 이 API는 프라이버시 보호 원칙(`FR-B-1.3`)에 따라 생성된 회고록을 서버에 저장하지 않으며, 오직 요청자에게만 일회성으로 반환합니다.

### 접근 권한
- 모든 인증된 사용자 (`employee`, `team_lead`, `dept_head`, `admin`)

### 요청 (Request)

#### 본문 (Body)
```json
{
  "start_date": "2025-01-01",
  "end_date": "2025-06-30"
}
```
- `start_date` (string, required): 회고록 생성 시작일 (YYYY-MM-DD 형식)
- `end_date` (string, required): 회고록 생성 종료일 (YYYY-MM-DD 형식)

### 성공 응답 (Response)

#### 상태 코드: `200 OK`
```json
{
  "content": "This is a mock summary of the following activities:\n\n--- Mock activities for jira account ---\n- Resolved ticket PROJECT-123: Fix login bug on 2025-01-01\n- Committed 'feat: Add new dashboard widget' on 2025-06-30\n- Reviewed pull request #456 from a colleague."
}
```
- `content` (string): AI가 생성한 회고록 텍스트

### 오류 응답 (Error Response)

#### 상태 코드: `401 Unauthorized`
- 인증되지 않은 사용자가 요청한 경우
```json
{
  "detail": "Not authenticated"
}
```

#### 상태 코드: `422 Unprocessable Entity`
- 요청 본문의 `start_date` 또는 `end_date` 형식이 잘못된 경우

```