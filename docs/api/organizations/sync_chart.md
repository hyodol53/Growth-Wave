# API Documentation: Organization and User Synchronization

## Endpoint: `POST /api/v1/organizations/sync-chart`

### Description

This endpoint allows an administrator to synchronize the entire organization chart and user database in a single operation by uploading a specifically formatted JSON file. The system will process the file to create or update organizations and users based on the provided data. The backend logic is handled by the `sync_organizations_and_users_from_json` function.

### Request

- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Authentication:** Requires Administrator privileges.
- **Body:** The request must contain a single file field.

#### Form Data

- **`file`**: The `.json` file containing the organization and user data.

### JSON File Structure

The JSON file must be an object containing two main keys: `organizations` and `users`.

- **`organizations`**: An array of organization objects. The order matters, as parent organizations should be defined before their children.
- **`users`**: An array of user objects.

#### `organization` Object

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | string | Yes | The name of the organization (e.g., "AI Solutions Team"). Must be unique. |
| `level` | integer | Yes | The hierarchical level (1: Center, 2: Office, 3: Team). |
| `parent_name`| string | No | The name of the parent organization. Must be `null` for top-level organizations (level 1). |

#### `user` Object

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `username` | string | Yes | The unique username for login. |
| `email` | string | Yes | The user's email address. |
| `full_name` | string | Yes | The user's full name. |
| `password` | string | Yes | The user's password. It's recommended to provide a temporary password for new users. |
| `role` | string | Yes | The user's role. Must be one of: `employee`, `team_lead`, `dept_head`, `admin`. The system may also adjust roles based on hierarchy. |
| `organization_name`| string | Yes | The name of the organization this user belongs to. Must match one of the organization names in the `organizations` array. |

#### Example JSON

```json
{
  "organizations": [
    {
      "name": "Advanced Research Center",
      "level": 1,
      "parent_name": null
    },
    {
      "name": "AI Solutions Office",
      "level": 2,
      "parent_name": "Advanced Research Center"
    },
    {
      "name": "Data Science Team",
      "level": 3,
      "parent_name": "AI Solutions Office"
    }
  ],
  "users": [
    {
      "username": "johndoe",
      "email": "john.doe@example.com",
      "full_name": "John Doe",
      "password": "temporary_password_123",
      "role": "employee",
      "organization_name": "Data Science Team"
    },
    {
      "username": "janesmith",
      "email": "jane.smith@example.com",
      "full_name": "Jane Smith",
      "password": "temporary_password_456",
      "role": "team_lead",
      "organization_name": "Data Science Team"
    }
  ]
}
```

### Responses

#### Success Response

- **Status Code:** `200 OK`
- **Content:** A JSON object (`Dict[str, Any]`) summarizing the result of the operation. The exact content depends on the `org_crud.sync_organizations_and_users_from_json` implementation.

**Example Success Response:**
```json
{
  "organizations": {
    "created": 5,
    "updated": 2,
    "skipped": 0
  },
  "users": {
    "created": 25,
    "updated": 8,
    "skipped": 2
  }
}
```

#### Error Responses

- **Status Code:** `400 Bad Request`
  - **Reason:** The uploaded file is not a JSON file.
  ```json
  {
    "detail": "Invalid file type. Only JSON is supported."
  }
  ```
- **Status Code:** `403 Forbidden`
  - **Reason:** The user making the request does not have administrator privileges.
  ```json
  {
    "detail": "Not authenticated or insufficient permissions."
  }
  ```
- **Status Code:** `500 Internal Server Error`
  - **Reason:** A generic error occurred during file processing or database operations. The detail message will contain more information about the specific error.
  ```json
  {
    "detail": "An unexpected error occurred: [error message from exception]"
  }
  ```
