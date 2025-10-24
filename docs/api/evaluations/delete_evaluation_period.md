### `DELETE /api/v1/evaluations/evaluation-periods/{period_id}`

**Description:** Deletes an evaluation period by its ID.

**Access:** Admin only.

**Path Parameters:**

- `period_id` (required, integer): The ID of the evaluation period to delete.

**Response:**

- **Code:** `200 OK`
- **Body:**

```json
{
  "name": "2025 First Half",
  "start_date": "2025-01-01",
  "end_date": "2025-06-30",
  "id": 1
}
```

**Errors:**

- `401 Unauthorized`: If the user is not authenticated.
- `403 Forbidden`: If the authenticated user is not an admin.
- `404 Not Found`: If an evaluation period with the specified `period_id` does not exist.
