# API Documentation: Department Evaluations

This document provides details on the APIs for managing department evaluations.

---

## 1. Upsert Department Evaluation

Creates a new department evaluation or updates an existing one for a specific evaluation period.

- **Endpoint:** `POST /api/v1/evaluations/department-evaluations/`
- **Permission:** `CENTER_HEAD`
- **Description:** This endpoint allows a Center Head to assign a grade (e.g., S, A, B) to a department (실) under their center for a given evaluation period. If an evaluation for that department and period already exists, it will be updated (upsert).

### Request Body

```json
{
  "department_id": 123,
  "grade": "A",
  "evaluation_period_id": 456
}
```

- `department_id` (integer, required): The ID of the department being evaluated.
- `grade` (string, required): The grade assigned to the department.
- `evaluation_period_id` (integer, required): The ID of the evaluation period this evaluation belongs to.

### Responses

- **200 OK (Success):** Returns the created or updated department evaluation object.
  ```json
  {
    "id": 1,
    "department_id": 123,
    "grade": "A",
    "evaluation_period_id": 456
  }
  ```
- **403 Forbidden:** If the user is not a `CENTER_HEAD` or does not have authority over the specified department.
- **422 Unprocessable Entity:** If the request body is invalid.

---

## 2. Get Department Evaluations for a Period

Retrieves a list of all department evaluations for a specific evaluation period.

- **Endpoint:** `GET /api/v1/evaluations/department-evaluations/`
- **Permission:** Authenticated User
- **Description:** Fetches all department evaluation records associated with a specific evaluation period ID.

### Query Parameters

- `evaluation_period_id` (integer, required): The ID of the evaluation period to filter the results.

**Example Request:**
`GET /api/v1/evaluations/department-evaluations/?evaluation_period_id=456`

### Responses

- **200 OK (Success):** Returns a list of department evaluation objects.
  ```json
  [
    {
      "id": 1,
      "department_id": 123,
      "grade": "A",
      "evaluation_period_id": 456
    },
    {
      "id": 2,
      "department_id": 124,
      "grade": "S",
      "evaluation_period_id": 456
    }
  ]
  ```
- **422 Unprocessable Entity:** If the `evaluation_period_id` parameter is missing or invalid.
