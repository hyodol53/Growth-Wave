# Create Qualitative Evaluations

**POST** `/api/v1/evaluations/qualitative-evaluations/`

## Description

Allows a Team Lead or Department Head to submit qualitative evaluations for their subordinates.

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
      "score": 95
    },
    {
      "evaluatee_id": 2,
      "score": 88
    }
  ]
}
```

- **evaluations** (List[QualitativeEvaluationBase], required): A list of evaluations to create.
  - **evaluatee_id** (int, required): The ID of the user being evaluated.
  - **score** (int, required): The score given to the user (must be between 0 and 100).

## Success Response

**Status Code:** `200 OK`

```json
[
  {
    "evaluatee_id": 1,
    "score": 95,
    "id": 1,
    "evaluator_id": 10,
    "evaluation_period": "2024-H2"
  },
  {
    "evaluatee_id": 2,
    "score": 88,
    "id": 2,
    "evaluator_id": 10,
    "evaluation_period": "2024-H2"
  }
]
```

## Error Responses

- **Status Code:** `400 Bad Request`
  - If the average score is out of the valid range (0-100).

- **Status Code:** `403 Forbidden`
  - If the user is not authenticated.
  - If the user does not have the required role (`TEAM_LEAD` or `DEPT_HEAD`).
  - If the user tries to evaluate someone who is not their subordinate.

- **Status Code:** `404 Not Found`
  - If the `evaluatee_id` does not exist.

- **Status Code:** `422 Unprocessable Entity`
  - If the request body is invalid.
