# POST /api/v1/evaluations/calculate

## API 설명

지정된 사용자 또는 현재 로그인한 부서장(DEPT_HEAD)의 하위 조직원 전체에 대한 최종 평가 점수를 계산하고 저장합니다. 이 엔드포인트는 평가 기간 내에 제출된 동료 평가, PM 평가, 정성 평가 데이터를 기반으로 직책별 가중치 및 프로젝트 참여 비중을 적용하여 최종 점수를 산출합니다. 계산된 결과는 `FinalEvaluation` 모델로 데이터베이스에 저장되거나 기존 기록이 업데이트됩니다.

## 접근 권한

-   `DEPT_HEAD` (부서장)
-   `ADMIN` (관리자)

## 요청 (Request)

-   **HTTP 메서드:** `POST`
-   **URL:** `/api/v1/evaluations/calculate`
-   **헤더:**
    -   `Authorization: Bearer <access_token>` (인증 토큰)
-   **본문 (Body):** `application/json`

    ```json
    {
      "user_ids": [
        1,  // 최종 평가를 계산할 사용자 ID 목록 (선택 사항)
        2
      ]
    }
    ```

    -   `user_ids` (List[integer], 선택 사항): 최종 평가를 계산할 사용자 ID 목록입니다. 이 필드가 제공되지 않으면, 호출자의 역할에 따라 다음과 같이 동작합니다.
        -   `DEPT_HEAD`: 현재 부서장의 모든 하위 조직원에 대해 계산합니다.
        -   `ADMIN`: 시스템 내 모든 활성 사용자에 대해 계산합니다.

## 응답 (Response)

-   **성공 응답 (Status: 200 OK):** `application/json`

    ```json
    [
      {
        "evaluatee_id": 1,
        "evaluation_period": "2025-H1",
        "peer_score": 76.0,
        "pm_score": 88.0,
        "qualitative_score": 95.0,
        "final_score": 85.8,
        "id": 1
      }
    ]
    ```

    -   `evaluatee_id` (integer): 평가 대상 사용자 ID.
    -   `evaluation_period` (string): 평가 기간 (예: "2025-H1").
    -   `peer_score` (float): 동료 평가 점수.
    -   `pm_score` (float): PM 평가 점수.
    -   `qualitative_score` (float): 정성 평가 점수.
    -   `final_score` (float): 최종 가중치 합산 점수.
    -   `id` (integer): 최종 평가 기록의 고유 ID.

-   **오류 응답:**
    -   **401 Unauthorized:** 유효한 인증 토큰이 제공되지 않았을 경우.
        ```json
        {
          "detail": "Not authenticated"
        }
        ```
    -   **403 Forbidden:** `DEPT_HEAD` 또는 `ADMIN` 권한이 없는 사용자가 접근했을 경우.
        ```json
        {
          "detail": "Not enough privileges to calculate final evaluations."
        }
        ```
    -   **422 Unprocessable Entity:** 요청 본문의 유효성 검사에 실패했을 경우 (예: `user_ids`가 유효한 정수 목록이 아님).
        ```json
        {
          "detail": [
            {
              "loc": ["body", "user_ids"],
              "msg": "value is not a valid list",
              "type": "type_error.list"
            }
          ]
        }
        ```