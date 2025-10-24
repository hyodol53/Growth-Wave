# Task 2.3: 평가 주기 및 등급 비율 API 버그 수정 및 안정화

이 문서는 이전에 `task_2_3_evaluation_period_and_ratio_api.md`에서 보고되었던, 평가 주기 관리 API의 `sqlalchemy.exc.StatementError` 버그를 해결하고 기능을 안정화한 과정을 기록합니다.

## 1. 문제 분석

이전 작업 로그와 테스트 재현을 통해 확인된 문제의 핵심 원인은 `app/crud/base.py`의 `CRUDBase` 클래스에 있었습니다.

- **초기 문제:** `create` 메서드에서 `jsonable_encoder`를 사용하여 Pydantic 모델을 딕셔너리로 변환했습니다. 이 과정에서 `datetime.date` 객체가 JSON 호환을 위해 날짜 문자열(예: "2025-01-01")로 다시 변환되었고, 이 문자열이 SQLAlchemy 모델에 전달되면서 데이터베이스 단에서 `TypeError`가 발생했습니다.

- **두 번째 문제:** 이 문제를 해결하기 위해 `jsonable_encoder(obj_in)`를 `obj_in.dict()`로 변경했으나, 이는 `obj_in`이 항상 Pydantic 모델일 것이라는 잘못된 가정에 기반했습니다. 일부 API 엔드포인트(`projects.py`)에서는 `create` 메서드에 순수 `dict` 객체를 전달하고 있었고, 이로 인해 `AttributeError: 'dict' object has no attribute 'dict'`라는 새로운 오류가 발생했습니다.

## 2. 해결 방안

`CRUDBase.create` 메서드가 Pydantic 모델과 순수 `dict` 타입을 모두 안전하게 처리할 수 있도록 로직을 보강했습니다.

- `isinstance(obj_in, BaseModel)`을 사용하여 `obj_in` 파라미터의 타입을 확인합니다.
- Pydantic `BaseModel`의 인스턴스일 경우, `obj_in.dict()`를 호출하여 딕셔너리로 변환합니다.
- `dict` 타입일 경우, 별도의 변환 없이 그대로 사용합니다.

```python
# in app/crud/base.py

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        if isinstance(obj_in, BaseModel):
            obj_in_data = obj_in.dict()
        else:
            obj_in_data = obj_in
        db_obj = self.model(**obj_in_data)
        # ...
```

## 3. 검증 및 결론

위와 같이 수정한 후 `poetry run pytest`를 실행하여 전체 테스트 스위트(60개)가 모두 성공적으로 통과하는 것을 확인했습니다.

이로써, 이전에 작업을 중단시켰던 평가 주기 및 등급 비율 설정 API(`FR-A-2.1`, `FR-A-2.2`) 관련 기능이 완전히 안정화되었음을 선언합니다.
