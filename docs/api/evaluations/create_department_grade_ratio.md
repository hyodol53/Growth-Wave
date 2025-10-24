### `POST /api/v1/evaluations/department-grade-ratios/`

**Description:** Creates a new department grade ratio setting.

**Access:** Admin only.

**Request Body:**

```json
{
  "department_grade": "S",
  "s_ratio": 0.6,
  "a_ratio": 0.4
}
```

**Response:**

- **Code:** `200 OK`
- **Body:**

```json
{
  "department_grade": "S",
  "s_ratio": 0.6,
  "a_ratio": 0.4,
  "id": 1
}
```

**Errors:**

- `401 Unauthorized`: If the user is not authenticated.
- `403 Forbidden`: If the authenticated user is not an admin.
- `422 Unprocessable Entity`: If the request body is invalid.
