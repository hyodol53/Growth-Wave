from typing import List

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import UserRole
from app.models.organization import Organization
from app.models.project import Project
from app.models.project_member import ProjectMember
from tests.utils.user import create_random_user, authentication_token_from_username

def create_organization(db: Session, name: str, level: int, parent_id: int = None) -> Organization:
    org = Organization(name=name, level=level, parent_id=parent_id)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

def create_project(db: Session, name: str, owner_org_id: int) -> Project:
    project = Project(name=name, owner_org_id=owner_org_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def test_set_project_member_weights_success(client: TestClient, db: Session):
    # Setup: Admin, Dept Head, Employee, Organization, Projects
    admin_user = create_random_user(db, role=UserRole.ADMIN)
    admin_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    # Create a department (level 2 organization)
    dept_org = create_organization(db, name="Development Dept", level=2)

    # Create a dept head in that department
    dept_head_user = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    dept_head_token_headers = authentication_token_from_username(client=client, username=dept_head_user.username, db=db)

    # Create an employee in the same department
    employee_user = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=dept_org.id)

    # Create projects owned by the department
    project1 = create_project(db, name="Project Alpha", owner_org_id=dept_org.id)
    project2 = create_project(db, name="Project Beta", owner_org_id=dept_org.id)
    project3 = create_project(db, name="Project Gamma", owner_org_id=dept_org.id)

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
    dept_org = create_organization(db, name="Another Dept", level=2)
    dept_head_user = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    dept_head_token_headers = authentication_token_from_username(client=client, username=dept_head_user.username, db=db)
    employee_user = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=dept_org.id)
    project1 = create_project(db, name="Project Delta", owner_org_id=dept_org.id)

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
    dept_org = create_organization(db, name="Sales Dept", level=2)
    employee_user = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=dept_org.id)
    employee_token_headers = authentication_token_from_username(client=client, username=employee_user.username, db=db)
    project1 = create_project(db, name="Project Epsilon", owner_org_id=dept_org.id)

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
    dept_org1 = create_organization(db, name="Dept A", level=2)
    dept_org2 = create_organization(db, name="Dept B", level=2)

    dept_head_user_a = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org1.id)
    dept_head_token_headers_a = authentication_token_from_username(client=client, username=dept_head_user_a.username, db=db)

    employee_user_b = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=dept_org2.id)

    project1 = create_project(db, name="Project Zeta", owner_org_id=dept_org2.id)

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
    dept_org = create_organization(db, name="NonExistentUser Dept", level=2)
    dept_head_user = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    dept_head_token_headers = authentication_token_from_username(client=client, username=dept_head_user.username, db=db)
    project1 = create_project(db, name="Project Eta", owner_org_id=dept_org.id)

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
    dept_org = create_organization(db, name="Update Test Dept", level=2)
    dept_head_user = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    dept_head_token_headers = authentication_token_from_username(client=client, username=dept_head_user.username, db=db)
    employee_user = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=dept_org.id)
    project1 = create_project(db, name="Project Iota", owner_org_id=dept_org.id)
    project2 = create_project(db, name="Project Kappa", owner_org_id=dept_org.id)

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
