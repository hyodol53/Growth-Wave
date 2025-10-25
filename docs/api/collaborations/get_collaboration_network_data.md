# API: 협업 네트워크 데이터 조회

## `GET /api/v1/collaborations/network-data`

### 설명
조직 또는 프로젝트를 기준으로 필터링된 협업 네트워크 시각화 데이터를 조회합니다. 이 데이터는 네트워크 그래프(노드 및 엣지)와 간단한 분석 정보(예: 가장 많은 리뷰를 한 사람)를 포함합니다.

### 접근 권한
- 인증된 모든 사용자 (`employee`, `team_lead`, `dept_head`, `admin`)

### 요청 (Request)

#### 쿼리 파라미터 (Query Parameters)
- `project_id` (integer, optional): 특정 프로젝트 ID를 기준으로 데이터를 필터링합니다.
- `organization_id` (integer, optional): 특정 조직 ID를 기준으로 데이터를 필터링합니다. 해당 조직 및 모든 하위 조직에 속한 사용자들의 상호작용을 포함합니다.

**참고:** `project_id` 또는 `organization_id` 중 하나는 반드시 제공되어야 합니다.

### 응답 (Response)

#### 성공 (Success)
- **상태 코드:** `200 OK`
- **본문 (Body):** `CollaborationData` 스키마
```json
{
  "graph": {
    "nodes": [
      {
        "id": 1,
        "label": "Alice",
        "value": 1
      },
      {
        "id": 2,
        "label": "Bob",
        "value": 1
      }
    ],
    "edges": [
      {
        "source": 1,
        "target": 2,
        "value": 5
      }
    ]
  },
  "analysis": {
    "most_reviews": [
      {
        "user_id": 2,
        "count": 8
      }
    ],
    "most_help": [
      {
        "user_id": 1,
        "count": 12
      }
    ]
  }
}
```

#### 오류 (Error)
- **상태 코드:** `400 Bad Request`
  - `project_id`와 `organization_id`가 모두 제공되지 않은 경우
  ```json
  {
    "detail": "Either project_id or organization_id must be provided."
  }
  ```
- **상태 코드:** `401 Unauthorized`
  - 인증되지 않은 사용자의 요청인 경우
- **상태 코드:** `422 Unprocessable Entity`
  - 쿼리 파라미터의 타입이 잘못된 경우
