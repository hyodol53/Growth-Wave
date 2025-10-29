from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import UserRole
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.organization import create_random_organization
from tests.utils.project import create_random_project
from app.crud import project_member as crud_pm

def test_create_project_by_dept_head_success(client: TestClient, db: Session):
    # Setup: Org A, Dept Head A, User A (as PM)
    org_a = create_random_organization(db, name="Org A")
    dept_head_a = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org_a.id)
    pm_user_a = create_random_user(db, organization_id=org_a.id)
    token_headers = authentication_token_from_username(client=client, username=dept_head_a.username, db=db)

    # Action
    project_data = {"name": "Project A", "description": "Test project", "pm_id": pm_user_a.id}
    response = client.post("/api/v1/projects/", headers=token_headers, json=project_data)

    # Assert
    assert response.status_code == 201
    created_project = response.json()
    assert created_project["name"] == "Project A"
    assert created_project["pm"]["id"] == pm_user_a.id

    # Verify that the PM was added to project_members
    pm_membership = crud_pm.project_member.get_by_user_and_project(
        db, user_id=pm_user_a.id, project_id=created_project["id"]
    )
    assert pm_membership is not None
    assert pm_membership.is_pm is True
    assert pm_membership.participation_weight == 100

def test_create_project_by_dept_head_forbidden(client: TestClient, db: Session):
    # Setup: Org A and B, Dept Head A, User B (as PM)
    org_a = create_random_organization(db, name="Org A")
    org_b = create_random_organization(db, name="Org B")
    dept_head_a = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org_a.id)
    pm_user_b = create_random_user(db, organization_id=org_b.id)
    token_headers = authentication_token_from_username(client=client, username=dept_head_a.username, db=db)

    # Action
    project_data = {"name": "Forbidden Project", "pm_id": pm_user_b.id}
    response = client.post("/api/v1/projects/", headers=token_headers, json=project_data)

    # Assert
    assert response.status_code == 403
    assert "from their own department" in response.json()["detail"]

def test_create_project_by_admin_success(client: TestClient, db: Session):
    # Setup: Admin, Org B, User B (as PM)
    admin_user = create_random_user(db, role=UserRole.ADMIN)
    org_b = create_random_organization(db, name="Org B")
    pm_user_b = create_random_user(db, organization_id=org_b.id)
    token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    # Action
    project_data = {"name": "Admin Project", "pm_id": pm_user_b.id}
    response = client.post("/api/v1/projects/", headers=token_headers, json=project_data)

    # Assert
    assert response.status_code == 201
    created_project = response.json()
    assert created_project["name"] == "Admin Project"
    assert created_project["pm"]["id"] == pm_user_b.id

    # Verify that the PM was added to project_members
    pm_membership = crud_pm.project_member.get_by_user_and_project(
        db, user_id=pm_user_b.id, project_id=created_project["id"]
    )
    assert pm_membership is not None
    assert pm_membership.is_pm is True
    assert pm_membership.participation_weight == 100

def test_create_project_with_nonexistent_pm(client: TestClient, db: Session):
    # Setup
    org_a = create_random_organization(db, name="Org A")
    dept_head_a = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org_a.id)
    token_headers = authentication_token_from_username(client=client, username=dept_head_a.username, db=db)

    # Action
    project_data = {"name": "Bad Project", "pm_id": 99999}
    response = client.post("/api/v1/projects/", headers=token_headers, json=project_data)

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_create_project_by_employee_forbidden(client: TestClient, db: Session):
    # Setup
    employee = create_random_user(db, role=UserRole.EMPLOYEE)
    token_headers = authentication_token_from_username(client=client, username=employee.username, db=db)

    # Action
    project_data = {"name": "Employee Project", "pm_id": employee.id}
    response = client.post("/api/v1/projects/", headers=token_headers, json=project_data)

    # Assert
    assert response.status_code == 403

def test_read_project_by_id(client: TestClient, db: Session):
    # Setup
    org = create_random_organization(db)
    pm = create_random_user(db, organization_id=org.id)
    project = create_random_project(db, pm_id=pm.id)
    user = create_random_user(db)
    token_headers = authentication_token_from_username(client=client, username=user.username, db=db)

    # Action
    response = client.get(f"/api/v1/projects/{project.id}", headers=token_headers)

    # Assert
    assert response.status_code == 200
    project_data = response.json()
    assert project_data["name"] == project.name
    assert "pm" in project_data
    assert project_data["pm"]["id"] == pm.id

def test_update_project_by_pm_dept_head_success(client: TestClient, db: Session):
    # Setup
    org_a = create_random_organization(db, name="Org A")
    dept_head_a = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org_a.id)
    pm_user_a = create_random_user(db, organization_id=org_a.id)
    project = create_random_project(db, pm_id=pm_user_a.id)
    token_headers = authentication_token_from_username(client=client, username=dept_head_a.username, db=db)

    # Action
    update_data = {"description": "Updated description"}
    response = client.put(f"/api/v1/projects/{project.id}", headers=token_headers, json=update_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["description"] == "Updated description"

def test_update_project_by_other_dept_head_forbidden(client: TestClient, db: Session):
    # Setup
    org_a = create_random_organization(db, name="Org A")
    org_b = create_random_organization(db, name="Org B")
    pm_user_a = create_random_user(db, organization_id=org_a.id)
    dept_head_b = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org_b.id)
    project = create_random_project(db, pm_id=pm_user_a.id)
    token_headers = authentication_token_from_username(client=client, username=dept_head_b.username, db=db)

    # Action
    update_data = {"description": "Forbidden update"}
    response = client.put(f"/api/v1/projects/{project.id}", headers=token_headers, json=update_data)

    # Assert
    assert response.status_code == 403

def test_update_project_pm_by_dept_head_forbidden(client: TestClient, db: Session):
    # Setup
    org_a = create_random_organization(db, name="Org A")
    org_b = create_random_organization(db, name="Org B")
    dept_head_a = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org_a.id)
    pm_user_a = create_random_user(db, organization_id=org_a.id)
    pm_user_b = create_random_user(db, organization_id=org_b.id)
    project = create_random_project(db, pm_id=pm_user_a.id)
    token_headers = authentication_token_from_username(client=client, username=dept_head_a.username, db=db)

    # Action
    update_data = {"pm_id": pm_user_b.id}
    response = client.put(f"/api/v1/projects/{project.id}", headers=token_headers, json=update_data)

    # Assert
    assert response.status_code == 403
    assert "assign a PM from their own department" in response.json()["detail"]

def test_delete_project_by_admin_success(client: TestClient, db: Session):
    # Setup
    org = create_random_organization(db)
    pm = create_random_user(db, organization_id=org.id)
    project = create_random_project(db, pm_id=pm.id)
    admin = create_random_user(db, role=UserRole.ADMIN)
    token_headers = authentication_token_from_username(client=client, username=admin.username, db=db)

    # Action
    response = client.delete(f"/api/v1/projects/{project.id}", headers=token_headers)

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == project.id

    # Verify deletion
    response = client.get(f"/api/v1/projects/{project.id}", headers=token_headers)
    assert response.status_code == 404


# --- Tests for GET /projects/ ---

def test_read_projects_by_admin(client: TestClient, db: Session):
    # Arrange
    admin = create_random_user(db, role="admin")
    org = create_random_organization(db)
    pm = create_random_user(db, organization_id=org.id)
    create_random_project(db, pm_id=pm.id)
    create_random_project(db, pm_id=pm.id)
    admin_token_headers = authentication_token_from_username(client=client, username=admin.username, db=db)

    # Act
    response = client.get("/api/v1/projects/", headers=admin_token_headers)

    # Assert
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_read_projects_by_dept_head(client: TestClient, db: Session):
    # Arrange
    # Dept A
    dept_a = create_random_organization(db, name="Dept A")
    dept_head_a = create_random_user(db, role="dept_head", organization_id=dept_a.id)
    pm_a = create_random_user(db, organization_id=dept_a.id)
    project_a = create_random_project(db, name="Project A", pm_id=pm_a.id)

    # Dept B
    dept_b = create_random_organization(db, name="Dept B")
    pm_b = create_random_user(db, organization_id=dept_b.id)
    project_b = create_random_project(db, name="Project B", pm_id=pm_b.id)

    dept_head_a_token_headers = authentication_token_from_username(client=client, username=dept_head_a.username, db=db)

    # Act
    response = client.get("/api/v1/projects/", headers=dept_head_a_token_headers)

    # Assert
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 1
    assert projects[0]["id"] == project_a.id
    assert projects[0]["name"] == "Project A"

def test_read_projects_by_employee_forbidden(client: TestClient, db: Session):
    # Arrange
    employee = create_random_user(db, role="employee")
    employee_token_headers = authentication_token_from_username(client=client, username=employee.username, db=db)

    # Act
    response = client.get("/api/v1/projects/", headers=employee_token_headers)

    # Assert
    assert response.status_code == 403


# --- Tests for POST /projects/{project_id}/members ---

def test_add_project_member_by_admin_success(client: TestClient, db: Session):
    # Arrange
    admin = create_random_user(db, role="admin")
    admin_token_headers = authentication_token_from_username(client=client, username=admin.username, db=db)

    # Dept A
    dept_a = create_random_organization(db, name="Dept A")
    pm_a = create_random_user(db, organization_id=dept_a.id)
    project_a = create_random_project(db, name="Project A", pm_id=pm_a.id)

    # Dept B
    dept_b = create_random_organization(db, name="Dept B")
    user_b = create_random_user(db, organization_id=dept_b.id)

    # Act
    add_member_payload = {"user_id": user_b.id}
    response = client.post(
        f"/api/v1/projects/{project_a.id}/members",
        headers=admin_token_headers,
        json=add_member_payload,
    )

    # Assert
    assert response.status_code == 200 # Assuming 200, could be 201
    member_data = response.json()
    assert member_data["user_id"] == user_b.id
    assert member_data["project_id"] == project_a.id