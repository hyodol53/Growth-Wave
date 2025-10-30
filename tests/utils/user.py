from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.core.config import settings
from app.crud.user import user as crud_user
from app.schemas.user import UserCreate
from app.models.user import UserRole, User
from tests.utils.utils import random_lower_string, random_email

def create_random_user(db: Session, *, password: str = "password", role: UserRole = UserRole.EMPLOYEE, organization_id: int = None) -> User:
    email = random_email()
    username = random_lower_string()
    full_name = random_lower_string().capitalize()
    user_in = UserCreate(username=username, email=email, password=password, role=role, organization_id=organization_id, full_name=full_name)
    return crud_user.create(db=db, obj_in=user_in)

def authentication_token_from_username(
    *, client: TestClient, username: str, db: Session
) -> dict[str, str]:
    """
    Return a valid token headers for the user.
    """
    password = "password"  # As defined in create_random_user
    user = crud_user.get_by_username(db, username=username)
    
    from app.core.security import get_password_hash
    user.hashed_password = get_password_hash(password)
    db.add(user)
    db.commit()

    login_data = {"username": user.username, "password": password}
    r = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
