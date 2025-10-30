# Create Qualitative Evaluations

**POST** `/api/v1/evaluations/qualitative-evaluations/`

## Description

Allows a Team Lead or Department Head to submit qualitative evaluations for their subordinates.
The evaluation consists of a qualitative score (max 20), a department contribution score (max 10), and written feedback.

## Permissions

- Requires authentication.
- The user must have the role of `TEAM_LEAD` or `DEPT_HEAD`.
- The user can only evaluate members of their own organization or its sub-organizations.

## Request Body

```json
{
  "evaluations": [
    {
      "evaluatee_id": 1,
      "qualitative_score": 18,
      "department_contribution_score": 9,
      "feedback": "프로젝트 마감 기한을 준수하고 높은 품질의 결과물을 전달하는 데 크게 기여했습니다."
    },
    {
      "evaluatee_id": 2,
      "qualitative_score": 15,
      "department_contribution_score": 7,
      "feedback": "팀 내 지식 공유에 적극적이며, 동료들의 성장을 돕는 멘토 역할을 훌륭히 수행했습니다."
    }
  ]
}
```

- **evaluations** (List[QualitativeEvaluationBase], required): A list of evaluations to create.
  - **evaluatee_id** (int, required): The ID of the user being evaluated.
  - **qualitative_score** (int, required): The qualitative score given to the user (must be between 0 and 20).
  - **department_contribution_score** (int, required): The department contribution score (must be between 0 and 10).
  - **feedback** (str, optional): Written feedback for the user.

## Success Response

**Status Code:** `200 OK`

```json
[
  {
    "evaluatee_id": 1,
    "qualitative_score": 18,
    "department_contribution_score": 9,
    "feedback": "프로젝트 마감 기한을 준수하고 높은 품질의 결과물을 전달하는 데 크게 기여했습니다.",
    "id": 1,
    "evaluator_id": 10,
    "evaluation_period": "2024-H2"
  },
  {
    "evaluatee_id": 2,
    "qualitative_score": 15,
    "department_contribution_score": 7,
    "feedback": "팀 내 지식 공유에 적극적이며, 동료들의 성장을 돕는 멘토 역할을 훌륭히 수행했습니다.",
    "id": 2,
    "evaluator_id": 10,
    "evaluation_period": "2024-H2"
  }
]
```

## Error Responses

- **Status Code:** `400 Bad Request`
  - If a score is out of its valid range.

- **Status Code:** `403 Forbidden`
  - If the user is not authenticated.
  - If the user does not have the required role (`TEAM_LEAD` or `DEPT_HEAD`).
  - If the user tries to evaluate someone who is not their subordinate.

- **Status Code:** `404 Not Found`
  - If the `evaluatee_id` does not exist.

- **Status Code:** `422 Unprocessable Entity`
  - If the request body is invalid.
