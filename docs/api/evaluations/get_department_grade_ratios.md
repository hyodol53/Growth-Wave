### `GET /api/v1/evaluations/department-grade-ratios/`

**Description:** Retrieves a list of all department grade ratio settings.

**Access:** Admin only.

**Query Parameters:**

- `skip` (optional, integer, default: 0): Number of records to skip.
- `limit` (optional, integer, default: 100): Maximum number of records to return.

**Response:**

- **Code:** `200 OK`
- **Body:**

```json
[
  {
    "department_grade": "S",
    "s_ratio": 0.6,
    "a_ratio": 0.4,
    "id": 1
  },
  {
    "department_grade": "A",
    "s_ratio": 0.4,
    "a_ratio": 0.2,
    "id": 2
  }
]
```

**Errors:**

- `401 Unauthorized`: If the user is not authenticated.
- `403 Forbidden`: If the authenticated user is not an admin.
