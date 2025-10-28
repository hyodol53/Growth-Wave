
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.organization import create_random_organization
from tests.utils.project import create_random_project
from tests.utils.project_member import create_project_member
from tests.utils.evaluation import create_random_evaluation_period, create_random_final_evaluation
from datetime import date

def test_create_user_by_admin(client: TestClient, db: Session):
    # Create an admin user and get token
    admin = create_random_user(db, role='admin')
    admin_token_headers = authentication_token_from_username(
        client=client, username=admin.username, db=db
    )

    # Create a new user
    new_user_data = {
        "username": "new_test_user",
        "email": "new_test_user@example.com",
        "password": "new_password"
    }
    response = client.post(
        f"/api/v1/users/",
        headers=admin_token_headers,
        json=new_user_data,
    )
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["email"] == new_user_data["email"]
    assert created_user["username"] == new_user_data["username"]

def test_update_user_by_admin(client: TestClient, db: Session):
    admin = create_random_user(db, role='admin')
    admin_token_headers = authentication_token_from_username(client=client, username=admin.username, db=db)
    
    user_to_update = create_random_user(db)
    org = create_random_organization(db)

    update_data = {"full_name": "Updated Name", "organization_id": org.id}
    response = client.put(
        f"/api/v1/users/{user_to_update.id}",
        headers=admin_token_headers,
        json=update_data,
    )
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["full_name"] == "Updated Name"
    assert updated_user["organization_id"] == org.id

def test_update_user_not_found(client: TestClient, db: Session):
    admin = create_random_user(db, role='admin')
    admin_token_headers = authentication_token_from_username(client=client, username=admin.username, db=db)
    
    update_data = {"full_name": "Updated Name"}
    response = client.put(
        f"/api/v1/users/99999",
        headers=admin_token_headers,
        json=update_data,
    )
    assert response.status_code == 404

def test_update_user_by_non_admin(client: TestClient, db: Session):
    user_to_update = create_random_user(db)
    non_admin = create_random_user(db, role='employee')
    non_admin_token_headers = authentication_token_from_username(client=client, username=non_admin.username, db=db)

    update_data = {"full_name": "Updated Name"}
    response = client.put(
        f"/api/v1/users/{user_to_update.id}",
        headers=non_admin_token_headers,
        json=update_data,
    )
    assert response.status_code == 403

def test_delete_user_by_admin(client: TestClient, db: Session):
    admin = create_random_user(db, role='admin')
    admin_token_headers = authentication_token_from_username(client=client, username=admin.username, db=db)
    
    user_to_delete = create_random_user(db)

    response = client.delete(
        f"/api/v1/users/{user_to_delete.id}",
        headers=admin_token_headers,
    )
    assert response.status_code == 200
    deleted_user = response.json()
    assert deleted_user["id"] == user_to_delete.id

def test_delete_user_not_found(client: TestClient, db: Session):
    admin = create_random_user(db, role='admin')
    admin_token_headers = authentication_token_from_username(client=client, username=admin.username, db=db)
    
    response = client.delete(
        f"/api/v1/users/99999",
        headers=admin_token_headers,
    )
    assert response.status_code == 404

def test_delete_user_by_non_admin(client: TestClient, db: Session):
    user_to_delete = create_random_user(db)
    non_admin = create_random_user(db, role='employee')
    non_admin_token_headers = authentication_token_from_username(client=client, username=non_admin.username, db=db)

    response = client.delete(
        f"/api/v1/users/{user_to_delete.id}",
        headers=non_admin_token_headers,
    )
    assert response.status_code == 403

def test_read_my_history(client: TestClient, db: Session):
    # Setup
    org = create_random_organization(db)
    user = create_random_user(db, organization_id=org.id)
    user_token_headers = authentication_token_from_username(client=client, username=user.username, db=db)

    period1 = create_random_evaluation_period(db, name="2024-H1", start_date=date(2024, 1, 1), end_date=date(2024, 6, 30))
    project1 = create_random_project(db, owner_org_id=org.id, start_date=date(2024, 2, 1), end_date=date(2024, 5, 31))
    create_project_member(db, user_id=user.id, project_id=project1.id, participation_weight=100)
    create_random_final_evaluation(db, evaluatee_id=user.id, evaluation_period=period1.name, final_score=95.5, grade="S")

    # Action
    response = client.get("/api/v1/users/me/history", headers=user_token_headers)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["history"]) > 0
    history_for_period1 = next((h for h in data["history"] if h["evaluation_period"] == "2024-H1"), None)
    assert history_for_period1 is not None
    assert history_for_period1["final_evaluation"]["grade"] == "S"
    assert len(history_for_period1["projects"]) == 1
    assert history_for_period1["projects"][0]["project_name"] == project1.name

def test_read_user_history_by_manager(client: TestClient, db: Session):
    # Setup
    dept = create_random_organization(db)
    manager = create_random_user(db, role="dept_head", organization_id=dept.id)
    manager_token_headers = authentication_token_from_username(client=client, username=manager.username, db=db)
    subordinate = create_random_user(db, organization_id=dept.id)
    period = create_random_evaluation_period(db, name="2025-H1", start_date=date(2025, 1, 1), end_date=date(2025, 6, 30))
    create_random_final_evaluation(db, evaluatee_id=subordinate.id, evaluation_period=period.name, final_score=85.0, grade="A")

    # Action
    response = client.get(f"/api/v1/users/{subordinate.id}/history", headers=manager_token_headers)

    # Assert
    assert response.status_code == 200
    data = response.json()
    history_for_period = next((h for h in data["history"] if h["evaluation_period"] == "2025-H1"), None)
    assert history_for_period is not None
    assert history_for_period["final_evaluation"]["grade"] == "A"

def test_read_user_history_unauthorized(client: TestClient, db: Session):
    # Setup
    user1 = create_random_user(db)
    user2 = create_random_user(db)
    user1_token_headers = authentication_token_from_username(client=client, username=user1.username, db=db)

    # Action
    response = client.get(f"/api/v1/users/{user2.id}/history", headers=user1_token_headers)

    # Assert
    assert response.status_code == 403

def test_read_my_subordinates_as_dept_head(client: TestClient, db: Session):
    # 1. Setup organization hierarchy
    center = create_random_organization(db, name="Center", level=1)
    dept = create_random_organization(db, name="Department", level=2, parent_id=center.id)
    team = create_random_organization(db, name="Team", level=3, parent_id=dept.id)
    other_dept = create_random_organization(db, name="Other Department", level=2, parent_id=center.id)

    # 2. Setup users
    dept_head = create_random_user(db, role="dept_head", organization_id=dept.id)
    team_lead = create_random_user(db, role="team_lead", organization_id=team.id)
    employee_in_team = create_random_user(db, role="employee", organization_id=team.id)
    employee_in_dept = create_random_user(db, role="employee", organization_id=dept.id)
    employee_in_other_dept = create_random_user(db, role="employee", organization_id=other_dept.id)

    # 3. Get token and make request
    dept_head_token = authentication_token_from_username(
        client=client, username=dept_head.username, db=db
    )
    response = client.get("/api/v1/users/me/subordinates", headers=dept_head_token)

    # 4. Assertions
    assert response.status_code == 200
    subordinates = response.json()
    assert len(subordinates) == 3

    subordinate_ids = {s["id"] for s in subordinates}
    assert team_lead.id in subordinate_ids
    assert employee_in_team.id in subordinate_ids
    assert employee_in_dept.id in subordinate_ids
    assert dept_head.id not in subordinate_ids
    assert employee_in_other_dept.id not in subordinate_ids


def test_read_my_subordinates_as_team_lead(client: TestClient, db: Session):
    # 1. Setup organization hierarchy
    center = create_random_organization(db, name="Center2", level=1)
    dept = create_random_organization(db, name="Department2", level=2, parent_id=center.id)
    team = create_random_organization(db, name="Team2", level=3, parent_id=dept.id)

    # 2. Setup users
    team_lead = create_random_user(db, role="team_lead", organization_id=team.id)
    employee_in_team = create_random_user(db, role="employee", organization_id=team.id)
    employee_in_dept = create_random_user(db, role="employee", organization_id=dept.id)

    # 3. Get token and make request
    team_lead_token = authentication_token_from_username(
        client=client, username=team_lead.username, db=db
    )
    response = client.get("/api/v1/users/me/subordinates", headers=team_lead_token)

    # 4. Assertions
    assert response.status_code == 200
    subordinates = response.json()
    assert len(subordinates) == 1
    assert subordinates[0]["id"] == employee_in_team.id


def test_read_my_subordinates_as_employee(client: TestClient, db: Session):
    # 1. Setup user
    employee = create_random_user(db, role="employee")
    employee_token = authentication_token_from_username(
        client=client, username=employee.username, db=db
    )

    # 2. Make request
    response = client.get("/api/v1/users/me/subordinates", headers=employee_token)

    # 3. Assertions
    assert response.status_code == 403
    assert "You do not have permission" in response.json()["detail"]
