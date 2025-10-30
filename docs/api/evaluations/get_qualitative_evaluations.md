# Get Qualitative Evaluations Data

**GET** `/api/v/evaluations/qualitative-evaluations/`

## Description

Retrieves the list of users to be qualitatively evaluated by the current user (evaluator). The list is filtered based on the evaluator's role. It also includes any previously submitted evaluation data for each user.

## Permissions

- Requires authentication.
- The user must have the role of `TEAM_LEAD` or `DEPT_HEAD`.

## Role-based Filtering Logic

- If the user is a `TEAM_LEAD`, this endpoint returns all their direct and indirect subordinates.
- If the user is a `DEPT_HEAD`, this endpoint returns only the subordinates who are `TEAM_LEAD`s.
- For any other role, it returns an empty list.

## Success Response

**Status Code:** `200 OK`

The response body will contain the status of the evaluation and a list of members to be evaluated.

```json
{
  "status": "IN_PROGRESS",
  "members_to_evaluate": [
    {
      "evaluatee_id": 15,
      "evaluatee_name": "김팀장",
      "title": "팀장",
      "organization_name": "개발1팀",
      "qualitative_score": 18,
      "department_contribution_score": 8,
      "feedback": "프로젝트 리딩 능력이 탁월하며, 팀원들의 성장을 적극적으로 지원함."
    },
    {
      "evaluatee_id": 22,
      "evaluatee_name": "박선임",
      "title": "선임연구원",
      "organization_name": "개발1팀",
      "qualitative_score": null,
      "department_contribution_score": null,
      "feedback": null
    }
  ]
}
```

- **status** (str): The overall status of the qualitative evaluation for the current user. Can be `NOT_STARTED`, `IN_PROGRESS`, or `COMPLETED`.
- **members_to_evaluate** (List[Object]): A list of members to evaluate.
  - **evaluatee_id** (int): The ID of the user being evaluated.
  - **evaluatee_name** (str): The full name of the user being evaluated.
  - **title** (str): The job title of the evaluatee.
  - **organization_name** (str): The name of the organization the evaluatee belongs to.
  - **qualitative_score** (int | null): The previously submitted qualitative score (0-20). `null` if not yet evaluated.
  - **department_contribution_score** (int | null): The previously submitted department contribution score (0-10). `null` if not yet evaluated.
  - **feedback** (str | null): The previously submitted written feedback. `null` if not yet evaluated.

## Error Responses

- **Status Code:** `403 Forbidden`
  - If the user is not authenticated.
