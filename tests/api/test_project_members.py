from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import UserRole
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.organization import create_random_organization
from tests.utils.project import create_random_project
from app.crud import project_member as crud_pm

def test_add_project_member_by_dept_head_success(client: TestClient, db: Session):
    # Arrange
    dept = create_random_organization(db)
    dept_head = create_random_user(db, role="dept_head", organization_id=dept.id)
    pm = create_random_user(db, organization_id=dept.id)
    member_to_add = create_random_user(db, organization_id=dept.id)
    project = create_random_project(db, pm_id=pm.id)
    dept_head_token = authentication_token_from_username(client=client, username=dept_head.username, db=db)
    payload = {"user_id": member_to_add.id, "is_pm": False}

    # Act
    response = client.post(f"/api/v1/projects/{project.id}/members", headers=dept_head_token, json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == member_to_add.id
    assert data["project_id"] == project.id
    assert data["participation_weight"] == 100 # First project, should be 100%

def test_add_project_member_auto_weight_calculation(client: TestClient, db: Session):
    # Arrange
    dept = create_random_organization(db)
    dept_head = create_random_user(db, role="dept_head", organization_id=dept.id)
    pm = create_random_user(db, organization_id=dept.id)
    member = create_random_user(db, organization_id=dept.id)
    project1 = create_random_project(db, pm_id=pm.id)
    project2 = create_random_project(db, pm_id=pm.id)
    dept_head_token = authentication_token_from_username(client=client, username=dept_head.username, db=db)
    
    # Add to first project (will get 60%)
    crud_pm.project_member.create(db, obj_in={"user_id": member.id, "project_id": project1.id, "participation_weight": 60})
    
    payload = {"user_id": member.id}

    # Act: Add to the second project
    response = client.post(f"/api/v1/projects/{project2.id}/members", headers=dept_head_token, json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == member.id
    assert data["project_id"] == project2.id
    assert data["participation_weight"] == 40 # 100 - 60 = 40

def test_add_project_member_with_zero_weight(client: TestClient, db: Session):
    # Arrange
    dept = create_random_organization(db)
    dept_head = create_random_user(db, role="dept_head", organization_id=dept.id)
    pm = create_random_user(db, organization_id=dept.id)
    member = create_random_user(db, organization_id=dept.id)
    project1 = create_random_project(db, pm_id=pm.id)
    project2 = create_random_project(db, pm_id=pm.id)
    dept_head_token = authentication_token_from_username(client=client, username=dept_head.username, db=db)
    
    crud_pm.project_member.create(db, obj_in={"user_id": member.id, "project_id": project1.id, "participation_weight": 100})
    
    payload = {"user_id": member.id}

    # Act
    response = client.post(f"/api/v1/projects/{project2.id}/members", headers=dept_head_token, json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["participation_weight"] == 0 # 100 - 100 = 0

def test_add_project_member_to_other_dept_project_forbidden(client: TestClient, db: Session):
    # Arrange
    dept1 = create_random_organization(db)
    dept2 = create_random_organization(db)
    dept_head1 = create_random_user(db, role="dept_head", organization_id=dept1.id)
    pm2 = create_random_user(db, organization_id=dept2.id) # PM in other dept
    member1 = create_random_user(db, organization_id=dept1.id)
    project_in_dept2 = create_random_project(db, pm_id=pm2.id)
    dept_head1_token = authentication_token_from_username(client=client, username=dept_head1.username, db=db)
    payload = {"user_id": member1.id}

    # Act
    response = client.post(f"/api/v1/projects/{project_in_dept2.id}/members", headers=dept_head1_token, json=payload)

    # Assert
    assert response.status_code == 403

def test_add_other_dept_member_forbidden(client: TestClient, db: Session):
    # Arrange
    dept1 = create_random_organization(db)
    dept2 = create_random_organization(db)
    dept_head1 = create_random_user(db, role="dept_head", organization_id=dept1.id)
    pm1 = create_random_user(db, organization_id=dept1.id)
    member_from_dept2 = create_random_user(db, organization_id=dept2.id)
    project = create_random_project(db, pm_id=pm1.id)
    dept_head1_token = authentication_token_from_username(client=client, username=dept_head1.username, db=db)
    payload = {"user_id": member_from_dept2.id}

    # Act
    response = client.post(f"/api/v1/projects/{project.id}/members", headers=dept_head1_token, json=payload)

    # Assert
    assert response.status_code == 403

def test_add_duplicate_project_member_conflict(client: TestClient, db: Session):
    # Arrange
    dept = create_random_organization(db)
    dept_head = create_random_user(db, role="dept_head", organization_id=dept.id)
    pm = create_random_user(db, organization_id=dept.id)
    member = create_random_user(db, organization_id=dept.id)
    project = create_random_project(db, pm_id=pm.id)
    dept_head_token = authentication_token_from_username(client=client, username=dept_head.username, db=db)
    
    # Add member once
    crud_pm.project_member.create(db, obj_in={"user_id": member.id, "project_id": project.id, "participation_weight": 100})
    
    payload = {"user_id": member.id}

    # Act: Try to add the same member again
    response = client.post(f"/api/v1/projects/{project.id}/members", headers=dept_head_token, json=payload)

    # Assert
    assert response.status_code == 409
    assert "already a member" in response.json()["detail"]
