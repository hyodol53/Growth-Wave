# [백엔드 개발 요청] 최종 점수 수동 계산 기능 API 개발

## 1. 요청 배경
- **요구사항 ID:** FR-A-4.7
- **요청자:** 프론트엔드 에이전트
- **요약:** 관리자가 '평가 결과 조회' 페이지에서 특정 평가 기간을 대상으로 **'최종 점수 계산'**을 수동으로 실행할 수 있는 기능이 요구사항에 추가되었습니다.
- **필요성:** 모든 평가 데이터가 정상적으로 제출되었는지 확인 후, 관리자가 원하는 특정 시점에 최종 점수 산출을 명시적으로 트리거하여 시스템 안정성을 확보하기 위함입니다.

## 2. 주요 기능 설명
- 관리자는 평가 기간을 선택하고, 버튼을 클릭하여 해당 기간에 속한 모든 평가 대상자의 최종 점수 계산을 서버에 요청합니다.
- 이 요청을 처리하기 위한 백엔드 API 엔드포인트 개발이 필요합니다.

## 3. 상세 API 명세
- **Method:** `POST`
- **URI:** `/api/v1/evaluation-periods/{evaluation_period_id}/calculate`
- **설명:** 특정 평가 기간(`evaluation_period_id`)에 속한 모든 평가 대상자의 최종 점수를 일괄적으로 계산하고 데이터베이스에 저장합니다.
- **Path Parameter:**
    - `evaluation_period_id` (integer, required): 최종 점수를 계산할 평가 기간의 고유 ID.
- **Request Body:** 없음 (Empty)
- **권한:** **관리자(Admin)** 역할이 있는 사용자만 호출할 수 있어야 합니다.
- **성공 응답 (Success Response):**
    - **Code:** `202 Accepted`
    - **Body:**
        ```json
        {
          "message": "Final score calculation for the evaluation period has been successfully initiated."
        }
        ```
- **실패 응답 (Error Response):**
    - **Code:** `403 Forbidden`
        - **사유:** 요청자가 관리자 권한을 가지고 있지 않은 경우.
    - **Code:** `404 Not Found`
        - **사유:** URI에 명시된 `evaluation_period_id`에 해당하는 평가 기간이 존재하지 않는 경우.
    - **Code:** `409 Conflict`
        - **사유:** 해당 평가 기간의 최종 점수 계산이 이미 진행 중이거나 완료된 상태일 경우.

## 4. 프론트엔드 개발 계획
- 상기 API가 개발 완료되면, 프론트엔드에서는 다음을 구현할 예정입니다.
    1. '평가 결과 조회' 페이지에 관리자 전용 '최종 점수 계산' 버튼 추가.
    2. 버튼 클릭 시, 현재 선택된 평가 기간 ID를 담아 본 API를 호출하는 로직 구현.
    3. API 호출 결과에 따른 사용자 피드백 처리.

감사합니다.
