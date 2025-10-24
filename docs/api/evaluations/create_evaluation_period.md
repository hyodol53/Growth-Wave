### `POST /api/v1/evaluations/evaluation-periods/`

**Description:** Creates a new evaluation period.

**Access:** Admin only.

**Request Body:**

```json
{
  "name": "2025-H1",
  "start_date": "2025-01-01",
  "end_date": "2025-06-30"
}
```

**Response:**

- **Code:** `200 OK`
- **Body:**

```json
{
  "name": "2025-H1",
  "start_date": "2025-01-01",
  "end_date": "2025-06-30",
  "id": 1
}
```

**Errors:**

- `401 Unauthorized`: If the user is not authenticated.
- `403 Forbidden`: If the authenticated user is not an admin.
- `422 Unprocessable Entity`: If the request body is invalid (e.g., missing fields, incorrect data types).
