# POST /api/v1/evaluation-periods/{evaluation_period_id}/calculate

## Description
관리자가 특정 평가 기간에 대한 최종 점수 계산을 수동으로 실행합니다.

이 API는 해당 평가 기간(`evaluation_period_id`)에 속한 모든 평가 대상자의 최종 점수를 일괄적으로 계산하고, 결과를 데이터베이스에 저장합니다. 이 작업은 비동기적으로 처리될 수 있습니다.

## Path Parameters
- **evaluation_period_id** (`integer`, required)
  - 최종 점수를 계산할 평가 기간의 고유 ID.

## Request Body
- 없음 (Empty)

## Permissions
- **관리자 (Admin)** 에게만 허용됩니다.

## Responses

### ✅ 202 Accepted
요청이 성공적으로 접수되었으며, 최종 점수 계산이 시작되었음을 나타냅니다.

**Body:**
```json
{
  "message": "Final score calculation for the evaluation period has been successfully initiated."
}
```

### ❌ 403 Forbidden
요청자가 해당 작업을 수행할 권한(관리자)을 가지고 있지 않습니다.

**Body:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### ❌ 404 Not Found
요청한 `evaluation_period_id`에 해당하는 평가 기간을 찾을 수 없습니다.

**Body:**
```json
{
  "detail": "Evaluation period not found."
}
```

### ❌ 409 Conflict
해당 평가 기간의 최종 점수 계산이 이미 진행 중이거나 완료된 상태입니다.

**Body:**
```json
{
  "detail": "Calculation for this evaluation period is already in progress or has been completed."
}
```
