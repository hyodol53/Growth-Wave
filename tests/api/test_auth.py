
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.user import UserCreate
from app.crud.user import user as crud_user
from app.models.user import UserRole

def test_login_for_access_token(client: TestClient, db: Session):
    # Create a user first
    admin_user_in = UserCreate(
        username="admin_test", 
        email="admin_test@example.com", 
        password="testpassword", 
        role=UserRole.ADMIN
    )
    crud_user.create(db, obj_in=admin_user_in)

    # Attempt to login
    login_data = {
        "username": "admin_test",
        "password": "testpassword",
    }
    response = client.post(f"/api/v1/auth/token", data=login_data)
    
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"
