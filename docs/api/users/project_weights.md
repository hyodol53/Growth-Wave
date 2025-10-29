# API Documentation: User Project Weights

This document provides details for the APIs used to manage a user's project participation weights.

---

## 1. Get User Project Weights

Retrieves the list of all projects a specific user is a member of, along with their participation weight for each project.

- **Method**: `GET`
- **Path**: `/api/v1/users/{user_id}/project-weights`
- **Permissions**: `Admin` or `Department Head` (can only view subordinates).

### Path Parameters

| Parameter | Type    | Description             |
| :-------- | :------ | :---------------------- |
| `user_id` | integer | The ID of the user to view. |

### Responses

- **`200 OK`**: Successful response.

  **Example Response Body:**
  ```json
  [
    {
      "project_id": 101,
      "project_name": "Project Alpha",
      "participation_weight": 60
    },
    {
      "project_id": 102,
      "project_name": "Project Beta",
      "participation_weight": 40
    }
  ]
  ```

- **`401 Unauthorized`**: Authentication token is missing or invalid.
- **`403 Forbidden`**: The current user does not have permission to view this user's weights.
- **`404 Not Found`**: The user with the specified `user_id` does not exist.

---

## 2. Update User Project Weights

Updates the participation weights for all projects a specific user is a member of. This is an overwrite operation; all of the user's project weights must be included in the request. The sum of all weights must be exactly 100.

- **Method**: `PUT`
- **Path**: `/api/v1/users/{user_id}/project-weights`
- **Permissions**: `Admin` or `Department Head` (can only update subordinates).

### Path Parameters

| Parameter | Type    | Description                   |
| :-------- | :------ | :---------------------------- |
| `user_id` | integer | The ID of the user to update. |

### Request Body

**Schema:** `UserProjectWeightsUpdate`

```json
{
  "weights": [
    {
      "project_id": 101,
      "participation_weight": 50
    },
    {
      "project_id": 102,
      "participation_weight": 50
    }
  ]
}
```

### Responses

- **`200 OK`**: Successful response. The body will contain the newly updated list of weights, in the same format as the `GET` endpoint.

- **`400 Bad Request`**: The validation fails. This occurs if the sum of `participation_weight` in the payload is not equal to 100.
  ```json
  {
    "detail": "Participation weights must sum to 100."
  }
  ```

- **`401 Unauthorized`**: Authentication token is missing or invalid.
- **`403 Forbidden`**: The current user does not have permission to update this user's weights.
- **`404 Not Found`**: The user with the specified `user_id` does not exist.
