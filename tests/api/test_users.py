
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.organization import create_random_organization

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
