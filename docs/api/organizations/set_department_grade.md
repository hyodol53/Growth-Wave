# 부서 평가 등급 설정 및 부서장 등급 동기화

**Endpoint:** `PUT /api/v1/organizations/{org_id}/grade`

**Description:** 특정 부서(실)의 평가 등급(S/A/B)을 설정합니다. 이 API가 호출되면, 해당 부서의 등급이 업데이트되고, 동시에 해당 부서의 장(실장)에게 동일한 최종 평가 등급이 자동으로 부여됩니다.

**Permission:** `CENTER_HEAD` 또는 `ADMIN` 역할이 필요합니다.

## Path Parameters

-   `org_id` (integer, required): 등급을 설정할 부서(실)의 고유 ID.

## Request Body

```json
{
  "department_grade": "S"
}
```

-   `department_grade` (string, required): 부서에 부여할 평가 등급. "S", "A", "B" 중 하나의 값이어야 합니다.

## Responses

### 200 OK: Successful Response

```json
{
  "id": 1,
  "name": "A실",
  "department_grade": "S",
  "parent_id": 10,
  "organization_level": 2
}
```

### 400 Bad Request: Invalid Grade

```json
{
  "detail": "Invalid grade provided. Must be one of 'S', 'A', 'B'."
}
```

### 403 Forbidden: Insufficient Permissions

```json
{
  "detail": "The user does not have sufficient privileges to perform this action."
}
```

### 404 Not Found: Organization Not Found

```json
{
  "detail": "Organization with id {org_id} not found."
}
```
