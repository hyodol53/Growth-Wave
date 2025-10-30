from typing import List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.organization import create_random_organization
from tests.utils.evaluation import create_random_evaluation_period, create_random_final_evaluation
from tests.utils.project import create_random_project
from tests.utils.project_member import create_project_member
from app.models.user import UserRole

def test_read_evaluated_users_by_period(client: TestClient, db: Session) -> None:
    # Setup
    admin_user = create_random_user(db, role=UserRole.ADMIN)
    dept_head_user = create_random_user(db, role=UserRole.DEPT_HEAD)
    employee_user = create_random_user(db, role=UserRole.EMPLOYEE)
    
    org = create_random_organization(db)
    dept_head_user.organization_id = org.id
    employee_user.organization_id = org.id
    db.add_all([dept_head_user, employee_user])
    db.commit()

    period = create_random_evaluation_period(db)
    create_random_final_evaluation(db, evaluatee_id=employee_user.id, period_id=period.id, final_score=90.0)

    admin_token_headers = authentication_token_from_username(
        client=client, username=admin_user.username, db=db
    )
    dept_head_token_headers = authentication_token_from_username(
        client=client, username=dept_head_user.username, db=db
    )

    # Test as Admin
    response_admin = client.get(
        f"{settings.API_V1_STR}/evaluations/periods/{period.id}/evaluated-users",
        headers=admin_token_headers,
    )
    assert response_admin.status_code == 200
    assert len(response_admin.json()) >= 1
    assert response_admin.json()[0]["user_id"] == employee_user.id

    # Test as Dept Head
    response_dept_head = client.get(
        f"{settings.API_V1_STR}/evaluations/periods/{period.id}/evaluated-users",
        headers=dept_head_token_headers,
    )
    assert response_dept_head.status_code == 200
    # This assumes get_subordinates works correctly
    assert len(response_dept_head.json()) >= 1 
    assert response_dept_head.json()[0]["user_id"] == employee_user.id

def test_read_detailed_evaluation_result_completed(client: TestClient, db: Session) -> None:
    # Setup
    admin_user = create_random_user(db, role=UserRole.ADMIN)
    dept_head_user = create_random_user(db, role=UserRole.DEPT_HEAD)
    employee_user = create_random_user(db, role=UserRole.EMPLOYEE)
    
    org = create_random_organization(db)
    dept_head_user.organization_id = org.id
    employee_user.organization_id = org.id
    db.add_all([dept_head_user, employee_user])
    db.commit()

    period = create_random_evaluation_period(db)
    project = create_random_project(db, pm_id=dept_head_user.id)
    create_project_member(db, user_id=employee_user.id, project_id=project.id)
    create_random_final_evaluation(db, evaluatee_id=employee_user.id, period_id=period.id, grade="A", final_score=95.5)

    admin_token_headers = authentication_token_from_username(
        client=client, username=admin_user.username, db=db
    )

    # Test
    response = client.get(
        f"{settings.API_V1_STR}/evaluations/periods/{period.id}/users/{employee_user.id}/details",
        headers=admin_token_headers,
    )
    data = response.json()
    
    assert response.status_code == 200
    assert data["status"] == "COMPLETED"
    assert data["user_info"]["user_id"] == employee_user.id
    assert data["final_evaluation"]["grade"] == "A"
    assert data["final_evaluation"]["final_score"] == 95.5
    assert len(data["project_evaluations"]) > 0

def test_read_detailed_evaluation_result_in_progress(client: TestClient, db: Session) -> None:
    # Setup
    admin_user = create_random_user(db, role=UserRole.ADMIN)
    employee_user = create_random_user(db)
    period = create_random_evaluation_period(db)

    admin_token_headers = authentication_token_from_username(
        client=client, username=admin_user.username, db=db
    )

    # Test
    response = client.get(
        f"{settings.API_V1_STR}/evaluations/periods/{period.id}/users/{employee_user.id}/details",
        headers=admin_token_headers,
    )
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "IN_PROGRESS"
    assert data["user_info"]["user_id"] == employee_user.id
    assert data["final_evaluation"] is None
    assert data["project_evaluations"] == []

def test_read_detailed_evaluation_result_permission_denied(client: TestClient, db: Session) -> None:
    # Setup
    dept_head_1 = create_random_user(db, role=UserRole.DEPT_HEAD)
    dept_head_2 = create_random_user(db, role=UserRole.DEPT_HEAD)
    employee_of_dept_2 = create_random_user(db)

    org1 = create_random_organization(db)
    org2 = create_random_organization(db)

    dept_head_1.organization_id = org1.id
    dept_head_2.organization_id = org2.id
    employee_of_dept_2.organization_id = org2.id
    db.add_all([dept_head_1, dept_head_2, employee_of_dept_2])
    db.commit()

    period = create_random_evaluation_period(db)

    dept_head_1_token_headers = authentication_token_from_username(
        client=client, username=dept_head_1.username, db=db
    )

    # Test: Dept Head 1 tries to access employee of Dept 2
    response = client.get(
        f"{settings.API_V1_STR}/evaluations/periods/{period.id}/users/{employee_of_dept_2.id}/details",
        headers=dept_head_1_token_headers,
    )
    assert response.status_code == 403