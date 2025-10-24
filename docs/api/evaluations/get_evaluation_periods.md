### `GET /api/v1/evaluations/evaluation-periods/`

**Description:** Retrieves a list of all evaluation periods.

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
    "name": "2025-H1",
    "start_date": "2025-01-01",
    "end_date": "2025-06-30",
    "id": 1
  },
  {
    "name": "2024-H2",
    "start_date": "2024-07-01",
    "end_date": "2024-12-31",
    "id": 2
  }
]
```

**Errors:**

- `401 Unauthorized`: If the user is not authenticated.
- `403 Forbidden`: If the authenticated user is not an admin.
