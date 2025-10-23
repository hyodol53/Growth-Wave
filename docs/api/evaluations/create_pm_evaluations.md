# Create PM Evaluations

- **HTTP Method:** `POST`
- **URL:** `/api/v1/evaluations/pm-evaluations/`

## Description

Project Managers (PMs) can submit evaluations for their project members. The API accepts a list of evaluations for one or more members within the same project.

## Permissions

- Only an authenticated user who is designated as a PM for the specified project can use this endpoint.
- If a non-PM user or a PM from a different project attempts to submit, the request will be rejected with a `403 Forbidden` error.

## Request

### Headers
- `Authorization: Bearer <JWT_TOKEN>`

### Body

The request body must be a JSON object containing a list of evaluations.

- **`evaluations`** (list[object], required): A list of evaluation objects.
    - **`project_id`** (integer, required): The ID of the project. All evaluations in the list must share the same project ID.
    - **`evaluatee_id`** (integer, required): The ID of the user being evaluated.
    - **`score`** (integer, required): The score given to the member. Must be between 0 and 100.

**Example:**
```json
{
  "evaluations": [
    {
      "project_id": 1,
      "evaluatee_id": 2,
      "score": 95
    },
    {
      "project_id": 1,
      "evaluatee_id": 3,
      "score": 88
    }
  ]
}
```

## Success Response

- **Status Code:** `200 OK`
- **Body:** A JSON array containing the created evaluation objects.

**Example:**
```json
[
  {
    "project_id": 1,
    "evaluatee_id": 2,
    "score": 95,
    "id": 1,
    "evaluator_id": 1,
    "evaluation_period": "2024-H2"
  },
  {
    "project_id": 1,
    "evaluatee_id": 3,
    "score": 88,
    "id": 2,
    "evaluator_id": 1,
    "evaluation_period": "2024-H2"
  }
]
```

## Error Responses

- **Status Code:** `400 Bad Request`
    - If scores are outside the 0-100 range.
    - If evaluations in the list belong to different projects.
- **Status Code:** `401 Unauthorized`
    - If the request is made without a valid JWT token.
- **Status Code:** `403 Forbidden`
    - If the user making the request is not the PM of the project.