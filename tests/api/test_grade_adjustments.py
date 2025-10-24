from typing import List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.user import UserRole
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.organization import create_random_organization
from tests.utils.evaluation import create_random_final_evaluation

def test_adjust_grades_as_dept_head_success(client: TestClient, db: Session) -> None:
    # 1. Create a department head and some users in their department
    dept_head_org = create_random_organization(db, department_grade="A")
    crud.department_grade_ratio.create(
        db, obj_in={"department_grade": "A", "s_ratio": 20.0, "a_ratio": 30.0}
    )
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_head_org.id)
    user1 = create_random_user(db, organization_id=dept_head_org.id)
    user2 = create_random_user(db, organization_id=dept_head_org.id)
    user3 = create_random_user(db, organization_id=dept_head_org.id)

    # 2. Create final evaluations for them
    evaluation_period = "2025-H1"
    eval1 = create_random_final_evaluation(db, evaluatee_id=user1.id, evaluation_period=evaluation_period, final_score=88.0, grade="B")
    eval2 = create_random_final_evaluation(db, evaluatee_id=user2.id, evaluation_period=evaluation_period, final_score=87.0, grade="B")
    eval3 = create_random_final_evaluation(db, evaluatee_id=user3.id, evaluation_period=evaluation_period, final_score=86.0, grade="B")

    # 3. Dept head logs in
    headers = authentication_token_from_username(client=client, username=dept_head.username, db=db)

    # 4. Perform adjustment (1 B+, 1 B-)
    adjustments = {
        "evaluation_period": evaluation_period,
        "adjustments": [
            {"user_id": user1.id, "grade": "B+"},
            {"user_id": user2.id, "grade": "B-"},
        ],
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/adjust-grades", headers=headers, json=adjustments)

    # 5. Assert success
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    grade_map = {item["evaluatee_id"]: item["grade"] for item in data}
    assert grade_map[user1.id] == "B+"
    assert grade_map[user2.id] == "B-"

    # 6. Verify in DB
    db.refresh(eval1)
    db.refresh(eval2)
    assert eval1.grade == "B+"
    assert eval2.grade == "B-"
    assert eval3.grade == "B" # Should be unchanged

def test_adjust_grades_b_plus_minus_imbalance(client: TestClient, db: Session) -> None:
    # 1. Create a department head and users
    dept_head_org = create_random_organization(db, department_grade="A")
    crud.department_grade_ratio.create(
        db, obj_in={"department_grade": "A", "s_ratio": 20.0, "a_ratio": 30.0}
    )
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_head_org.id)
    user1 = create_random_user(db, organization_id=dept_head_org.id)

    # 2. Create final evaluations
    evaluation_period = "2025-H1"
    create_random_final_evaluation(db, evaluatee_id=user1.id, evaluation_period=evaluation_period, final_score=88.0, grade="B")

    # 3. Dept head logs in
    headers = authentication_token_from_username(client=client, username=dept_head.username, db=db)

    # 4. Perform adjustment (only B+)
    adjustments = {
        "evaluation_period": evaluation_period,
        "adjustments": [{"user_id": user1.id, "grade": "B+"}],
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/adjust-grades", headers=headers, json=adjustments)

    # 5. Assert failure
    assert response.status_code == 400
    assert "The number of B+ and B- grades must be equal" in response.text

def test_adjust_grades_dept_head_outside_org(client: TestClient, db: Session) -> None:
    # 1. Create two departments
    org1 = create_random_organization(db, department_grade="A")
    crud.department_grade_ratio.create(
        db, obj_in={"department_grade": "A", "s_ratio": 20.0, "a_ratio": 30.0}
    )
    org2 = create_random_organization(db)
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org1.id)
    other_user = create_random_user(db, organization_id=org2.id)

    # 2. Create final evaluation for the user in the other department
    evaluation_period = "2025-H1"
    create_random_final_evaluation(db, evaluatee_id=other_user.id, evaluation_period=evaluation_period, final_score=88.0, grade="B")

    # 3. Dept head logs in
    headers = authentication_token_from_username(client=client, username=dept_head.username, db=db)

    # 4. Attempt to adjust grade for user in other department
    adjustments = {
        "evaluation_period": evaluation_period,
        "adjustments": [{"user_id": other_user.id, "grade": "B+"}],
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/adjust-grades", headers=headers, json=adjustments)

    # 5. Assert failure (The logic inside adjust_grades_for_department will not find the user and return empty list)
    assert response.status_code == 200
    assert response.json() == []

def test_adjust_grades_as_employee_unauthorized(client: TestClient, db: Session) -> None:
    # 1. Create a regular employee
    employee = create_random_user(db, role=UserRole.EMPLOYEE)
    headers = authentication_token_from_username(client=client, username=employee.username, db=db)

    # 2. Attempt to adjust grades
    adjustments = {
        "evaluation_period": "2025-H1",
        "adjustments": [{"user_id": 1, "grade": "B+"}],
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/adjust-grades", headers=headers, json=adjustments)

    # 3. Assert failure
    assert response.status_code == 403

def test_adjust_grades_as_admin_success(client: TestClient, db: Session, superuser_token_headers: dict) -> None:
    # 1. Create users in a department
    org = create_random_organization(db)
    user1 = create_random_user(db, organization_id=org.id)
    user2 = create_random_user(db, organization_id=org.id)

    # 2. Create final evaluations
    evaluation_period = "2025-H1"
    create_random_final_evaluation(db, evaluatee_id=user1.id, evaluation_period=evaluation_period, final_score=95.0, grade="A")
    create_random_final_evaluation(db, evaluatee_id=user2.id, evaluation_period=evaluation_period, final_score=85.0, grade="B")

    # 3. Admin performs adjustment
    adjustments = {
        "evaluation_period": evaluation_period,
        "adjustments": [
            {"user_id": user1.id, "grade": "S"},
            {"user_id": user2.id, "grade": "B+"},
        ],
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/adjust-grades", headers=superuser_token_headers, json=adjustments)

    # 4. Assert success
    assert response.status_code == 200
    data = response.json()
    grade_map = {item["evaluatee_id"]: item["grade"] for item in data}
    assert grade_map[user1.id] == "S"
    assert grade_map[user2.id] == "B+"

def test_adjust_grades_exceed_s_grade_to(client: TestClient, db: Session) -> None:
    # 1. Create department and users
    dept_org = create_random_organization(db, department_grade="S")
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    user1 = create_random_user(db, organization_id=dept_org.id)
    user2 = create_random_user(db, organization_id=dept_org.id)

    # 2. Create grade ratio (10% for S grade -> 0 for 2 employees)
    crud.department_grade_ratio.create(
        db, obj_in={"department_grade": "S", "s_ratio": 10.0, "a_ratio": 20.0}
    )

    # 3. Create final evaluations
    evaluation_period = "2025-H1"
    create_random_final_evaluation(db, evaluatee_id=user1.id, evaluation_period=evaluation_period, final_score=95.0, grade="A")
    create_random_final_evaluation(db, evaluatee_id=user2.id, evaluation_period=evaluation_period, final_score=94.0, grade="A")

    # 4. Dept head logs in
    headers = authentication_token_from_username(client=client, username=dept_head.username, db=db)

    # 5. Attempt to adjust more S grades than allowed
    adjustments = {
        "evaluation_period": evaluation_period,
        "adjustments": [
            {"user_id": user1.id, "grade": "S"},
        ],
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/adjust-grades", headers=headers, json=adjustments)

    # 6. Assert failure
    assert response.status_code == 400
    assert "Number of S grades (1) exceeds the limit (0)" in response.text
