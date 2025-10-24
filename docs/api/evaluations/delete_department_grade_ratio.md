### `DELETE /api/v1/evaluations/department-grade-ratios/{ratio_id}`

**Description:** Deletes a department grade ratio setting by its ID.

**Access:** Admin only.

**Path Parameters:**

- `ratio_id` (required, integer): The ID of the ratio setting to delete.

**Response:**

- **Code:** `200 OK`
- **Body:**

```json
{
  "department_grade": "S",
  "s_ratio": 0.65,
  "a_ratio": 0.35,
  "id": 1
}
```

**Errors:**

- `401 Unauthorized`: If the user is not authenticated.
- `403 Forbidden`: If the authenticated user is not an admin.
- `404 Not Found`: If a ratio setting with the specified `ratio_id` does not exist.
