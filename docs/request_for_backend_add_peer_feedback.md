# [백엔드 개발 요청] 상세 평가 결과 API에 동료 피드백 데이터 추가

## 1. 요청 배경
- **요구사항 ID:** FR-A-3.2, FR-A-5.3
- **요청자:** 프론트엔드 에이전트
- **요약:** 관리자가 '상세 평가 결과' 조회 시, 정성 평가 피드백뿐만 아니라 **프로젝트별 동료 평가 피드백**도 함께 확인할 수 있어야 한다는 요구사항이 있습니다.
- **필요성:** 현재 상세 평가 결과 API 응답에는 동료 평가 피드백 데이터가 포함되어 있지 않아 프론트엔드에서 이를 표시할 수 없습니다.

## 2. 요청 상세 내용
- **대상 API:** `GET /api/v1/evaluations/periods/{periodId}/users/{userId}/details`
- **변경 요청:**
    - API 응답 본문의 `project_evaluations` 배열에 포함된 **각 프로젝트 객체 내에** `peer_feedback` 필드를 추가해 주십시오.

## 3. 필드 명세
- **필드명:** `peer_feedback`
- **위치:** `project_evaluations` 배열 내의 각 객체
- **타입:** `string[]` (문자열 배열)
- **설명:**
    - 특정 프로젝트(`project_id`) 내에서, 해당 피평가자(`userId`)가 받은 **모든 동료 평가의 서술형 피드백**을 담고 있는 문자열 배열이어야 합니다.
    - 각 배열의 요소는 한 명의 동료가 작성한 피드백 원문입니다.
    - 만약 받은 피드백이 없다면, 빈 배열(`[]`)로 반환해 주십시오.

## 4. 응답 데이터 구조 예시 (변경 후)

```json
{
  "user_info": { ... },
  "final_evaluation": { ... },
  "qualitative_evaluation": { ... },
  "project_evaluations": [
    {
      "project_id": 101,
      "project_name": "Growth-Wave 개발",
      "participation_weight": 60,
      "peer_evaluation_score": 85.5,
      "pm_evaluation_score": 90.0,
      "peer_feedback": [  // <-- [!!] 이 필드를 추가 요청합니다.
        "항상 꼼꼼하게 테스트 케이스를 작성해주셔서 안정성이 크게 향상되었습니다.",
        "새로운 기술을 도입할 때 주도적으로 학습하고 팀에 공유해주셔서 좋았습니다."
      ]
    },
    {
      "project_id": 102,
      "project_name": "사내 인트라넷 유지보수",
      "participation_weight": 40,
      "peer_evaluation_score": 88.0,
      "pm_evaluation_score": 85.0,
      "peer_feedback": [ // <-- [!!] 이 프로젝트에 해당하는 피드백만 포함
        "이슈 발생 시 빠르게 원인을 파악하고 해결하는 능력이 탁월합니다."
      ]
    },
    {
      "project_id": 103,
      "project_name": "신규 입사자 멘토링",
      "participation_weight": 0,
      "peer_evaluation_score": 95.0,
      "pm_evaluation_score": 92.0,
      "peer_feedback": [] // <-- [!!] 피드백이 없는 경우 빈 배열
    }
  ],
  "status": "COMPLETED"
}
```

## 5. 프론트엔드 개발 계획
- 상기 API 변경이 완료되면, 프론트엔드에서는 상세 평가 결과 다이얼로그 내에서 각 프로젝트별로 동료 평가 피드백을 조회할 수 있도록 UI를 개발할 예정입니다.

감사합니다.
