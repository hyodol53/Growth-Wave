
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from tests.utils.user import create_random_user, authentication_token_from_username

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
