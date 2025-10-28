from typing import List

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import UserRole
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.organization import create_random_organization
from tests.utils.project import create_random_project
from app.models.project_member import ProjectMember
from app.schemas.project_member import ProjectMemberCreate
from app.crud import project_member as crud_pm


def test_set_project_member_weights_success(client: TestClient, db: Session):
    # Setup: Admin, Dept Head, Employee, Organization, Projects
    admin_user = create_random_user(db, role=UserRole.ADMIN)
    admin_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    # Create a department (level 2 organization)
    dept_org = create_random_organization(db, name="Development Dept", level=2)

    # Create a dept head in that department
    dept_head_user = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    dept_head_token_headers = authentication_token_from_username(client=client, username=dept_head_user.username, db=db)

    # Create an employee in the same department
    employee_user = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=dept_org.id)

    # Create projects owned by the department
    project1 = create_random_project(db, name="Project Alpha", owner_org_id=dept_org.id)
    project2 = create_random_project(db, name="Project Beta", owner_org_id=dept_org.id)
    project3 = create_random_project(db, name="Project Gamma", owner_org_id=dept_org.id)

    # Test data: employee participates in Project Alpha (50%) and Project Beta (50%)
    weights_data = {
        "user_id": employee_user.id,
        "weights": [
            {"project_id": project1.id, "participation_weight": 50},
            {"project_id": project2.id, "participation_weight": 50},
        ],
    }

    response = client.post(
        "/api/v1/projects/members/weights",
        headers=dept_head_token_headers,
        json=weights_data,
    )

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2

    # Verify database entries
    pm1 = db.query(ProjectMember).filter_by(user_id=employee_user.id, project_id=project1.id).first()
    pm2 = db.query(ProjectMember).filter_by(user_id=employee_user.id, project_id=project2.id).first()
    assert pm1 is not None
    assert pm1.participation_weight == 50
    assert pm2 is not None
    assert pm2.participation_weight == 50


def test_set_project_member_weights_invalid_total(client: TestClient, db: Session):
    # Setup
    dept_org = create_random_organization(db, name="Another Dept", level=2)
    dept_head_user = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    dept_head_token_headers = authentication_token_from_username(client=client, username=dept_head_user.username, db=db)
    employee_user = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=dept_org.id)
    project1 = create_random_project(db, name="Project Delta", owner_org_id=dept_org.id)

    # Test data: total weight not 100%
    weights_data = {
        "user_id": employee_user.id,
        "weights": [
            {"project_id": project1.id, "participation_weight": 60},
            {"project_id": project1.id, "participation_weight": 30}, # Total 90
        ],
    }

    response = client.post(
        "/api/v1/projects/members/weights",
        headers=dept_head_token_headers,
        json=weights_data,
    )

    assert response.status_code == 400
    assert "Total participation weight must be 100" in response.json()["detail"]


def test_set_project_member_weights_unauthorized_role(client: TestClient, db: Session):
    # Setup
    dept_org = create_random_organization(db, name="Sales Dept", level=2)
    employee_user = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=dept_org.id)
    employee_token_headers = authentication_token_from_username(client=client, username=employee_user.username, db=db)
    project1 = create_random_project(db, name="Project Epsilon", owner_org_id=dept_org.id)

    # Test data
    weights_data = {
        "user_id": employee_user.id,
        "weights": [
            {"project_id": project1.id, "participation_weight": 100},
        ],
    }

    response = client.post(
        "/api/v1/projects/members/weights",
        headers=employee_token_headers, # Employee trying to set weights
        json=weights_data,
    )

    assert response.status_code == 403
    assert "doesn't have enough privileges" in response.json()["detail"]


def test_set_project_member_weights_unauthorized_department(client: TestClient, db: Session):
    # Setup
    dept_org1 = create_random_organization(db, name="Dept A", level=2)
    dept_org2 = create_random_organization(db, name="Dept B", level=2)

    dept_head_user_a = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org1.id)
    dept_head_token_headers_a = authentication_token_from_username(client=client, username=dept_head_user_a.username, db=db)

    employee_user_b = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=dept_org2.id)

    project1 = create_random_project(db, name="Project Zeta", owner_org_id=dept_org2.id)

    # Test data: Dept Head A tries to set weights for Employee B (different department)
    weights_data = {
        "user_id": employee_user_b.id,
        "weights": [
            {"project_id": project1.id, "participation_weight": 100},
        ],
    }

    response = client.post(
        "/api/v1/projects/members/weights",
        headers=dept_head_token_headers_a,
        json=weights_data,
    )

    assert response.status_code == 403
    assert "only set weights for users in your own department" in response.json()["detail"]


def test_set_project_member_weights_non_existent_user(client: TestClient, db: Session):
    # Setup
    dept_org = create_random_organization(db, name="NonExistentUser Dept", level=2)
    dept_head_user = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    dept_head_token_headers = authentication_token_from_username(client=client, username=dept_head_user.username, db=db)
    project1 = create_random_project(db, name="Project Eta", owner_org_id=dept_org.id)

    # Test data: non-existent user_id
    weights_data = {
        "user_id": 99999, # Non-existent ID
        "weights": [
            {"project_id": project1.id, "participation_weight": 100},
        ],
    }

    response = client.post(
        "/api/v1/projects/members/weights",
        headers=dept_head_token_headers,
        json=weights_data,
    )

    assert response.status_code == 404
    assert "Target user not found" in response.json()["detail"]


def test_set_project_member_weights_update_existing(client: TestClient, db: Session):
    # Setup
    dept_org = create_random_organization(db, name="Update Test Dept", level=2)
    dept_head_user = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    dept_head_token_headers = authentication_token_from_username(client=client, username=dept_head_user.username, db=db)
    employee_user = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=dept_org.id)
    project1 = create_random_project(db, name="Project Iota", owner_org_id=dept_org.id)
    project2 = create_random_project(db, name="Project Kappa", owner_org_id=dept_org.id)

    # Initial weights
    initial_weights_data = {
        "user_id": employee_user.id,
        "weights": [
            {"project_id": project1.id, "participation_weight": 100},
        ],
    }
    client.post(
        "/api/v1/projects/members/weights",
        headers=dept_head_token_headers,
        json=initial_weights_data,
    )

    # Update weights
    updated_weights_data = {
        "user_id": employee_user.id,
        "weights": [
            {"project_id": project1.id, "participation_weight": 60},
            {"project_id": project2.id, "participation_weight": 40},
        ],
    }

    response = client.post(
        "/api/v1/projects/members/weights",
        headers=dept_head_token_headers,
        json=updated_weights_data,
    )

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2

    # Verify database entries are updated/created correctly
    pm1 = db.query(ProjectMember).filter_by(user_id=employee_user.id, project_id=project1.id).first()
    pm2 = db.query(ProjectMember).filter_by(user_id=employee_user.id, project_id=project2.id).first()
    assert pm1 is not None
    assert pm1.participation_weight == 60
    assert pm2 is not None
    assert pm2.participation_weight == 40

    # Ensure old entry for project1 is updated, not duplicated, and project2 is new
    all_memberships = db.query(ProjectMember).filter_by(user_id=employee_user.id).all()
    assert len(all_memberships) == 2


# Project CRUD Tests
def test_create_project_by_dept_head(client: TestClient, db: Session):
    dept_org = create_random_organization(db, name="R&D Dept", level=2)
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    dept_head_token_headers = authentication_token_from_username(client=client, username=dept_head.username, db=db)

    project_data = {"name": "New Core Tech Project", "owner_org_id": dept_org.id}
    response = client.post("/api/v1/projects/", headers=dept_head_token_headers, json=project_data)
    
    assert response.status_code == 201
    created_project = response.json()
    assert created_project["name"] == project_data["name"]
    assert created_project["owner_org_id"] == dept_org.id

def test_create_project_by_admin(client: TestClient, db: Session):
    admin = create_random_user(db, role=UserRole.ADMIN)
    admin_token_headers = authentication_token_from_username(client=client, username=admin.username, db=db)
    other_org = create_random_organization(db, name="Other Dept", level=2)

    project_data = {"name": "Admin Created Project", "owner_org_id": other_org.id}
    response = client.post("/api/v1/projects/", headers=admin_token_headers, json=project_data)
    
    assert response.status_code == 201
    assert response.json()["name"] == project_data["name"]

def test_create_project_unauthorized_role(client: TestClient, db: Session):
    org = create_random_organization(db, name="Unauthorized Dept", level=2)
    employee = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=org.id)
    employee_token_headers = authentication_token_from_username(client=client, username=employee.username, db=db)

    project_data = {"name": "Unauthorized Project", "owner_org_id": org.id}
    response = client.post("/api/v1/projects/", headers=employee_token_headers, json=project_data)
    
    assert response.status_code == 403

def test_read_projects(client: TestClient, db: Session):
    org = create_random_organization(db)
    create_random_project(db, owner_org_id=org.id)
    user = create_random_user(db)
    user_token_headers = authentication_token_from_username(client=client, username=user.username, db=db)

    response = client.get("/api/v1/projects/", headers=user_token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_update_project_by_owner_dept_head(client: TestClient, db: Session):
    dept_org = create_random_organization(db)
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    dept_head_token_headers = authentication_token_from_username(client=client, username=dept_head.username, db=db)
    project = create_random_project(db, owner_org_id=dept_org.id)

    update_data = {"name": "Updated Project Name"}
    response = client.put(f"/api/v1/projects/{project.id}", headers=dept_head_token_headers, json=update_data)
    
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Project Name"

def test_update_project_by_other_dept_head(client: TestClient, db: Session):
    org1 = create_random_organization(db, name="Org 1")
    org2 = create_random_organization(db, name="Org 2")
    dept_head_2 = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org2.id)
    dept_head_2_token_headers = authentication_token_from_username(client=client, username=dept_head_2.username, db=db)
    project_in_org1 = create_random_project(db, owner_org_id=org1.id)

    update_data = {"name": "Illegal Update"}
    response = client.put(f"/api/v1/projects/{project_in_org1.id}", headers=dept_head_2_token_headers, json=update_data)
    
    assert response.status_code == 403

def test_delete_project_by_admin(client: TestClient, db: Session):
    admin = create_random_user(db, role=UserRole.ADMIN)
    admin_token_headers = authentication_token_from_username(client=client, username=admin.username, db=db)
    org = create_random_organization(db)
    project = create_random_project(db, owner_org_id=org.id)

    response = client.delete(f"/api/v1/projects/{project.id}", headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json()["id"] == project.id

    # Verify it's deleted
    response = client.get(f"/api/v1/projects/{project.id}", headers=admin_token_headers)
    assert response.status_code == 404

def test_read_project_members(client: TestClient, db: Session):
    # Setup: An organization, a project, and a user to make the request
    org = create_random_organization(db)
    requesting_user = create_random_user(db, organization_id=org.id)
    user_token_headers = authentication_token_from_username(
        client=client, username=requesting_user.username, db=db
    )
    project = create_random_project(db, owner_org_id=org.id)

    # Create two members for the project
    member1 = create_random_user(db, organization_id=org.id)
    member2 = create_random_user(db, organization_id=org.id)

    crud_pm.project_member.create(db, obj_in=ProjectMemberCreate(
        user_id=member1.id,
        project_id=project.id,
        is_pm=True,
        participation_weight=60
    ))
    crud_pm.project_member.create(db, obj_in=ProjectMemberCreate(
        user_id=member2.id,
        project_id=project.id,
        is_pm=False,
        participation_weight=40
    ))

    # Make the API call
    response = client.get(
        f"/api/v1/projects/{project.id}/members", headers=user_token_headers
    )

    # Assertions
    assert response.status_code == 200
    members_list = response.json()
    assert len(members_list) == 2
    
    # Create a dict for easy lookup
    members = {m['user_id']: m for m in members_list}

    assert members[member1.id]["full_name"] == member1.full_name
    assert members[member1.id]["is_pm"] is True
    assert members[member1.id]["participation_weight"] == 60

    assert members[member2.id]["full_name"] == member2.full_name
    assert members[member2.id]["is_pm"] is False
    assert members[member2.id]["participation_weight"] == 40


def test_read_project_members_not_found(client: TestClient, db: Session):
    user = create_random_user(db)
    user_token_headers = authentication_token_from_username(
        client=client, username=user.username, db=db
    )
    non_existent_project_id = 99999
    response = client.get(
        f"/api/v1/projects/{non_existent_project_id}/members", headers=user_token_headers
    )
    assert response.status_code == 404
    assert "Project not found" in response.json()["detail"]
