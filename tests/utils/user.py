from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import random
import string

from app.crud.user import user as crud_user
from app.schemas.user import UserCreate
from app.models.user import UserRole, User

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))

def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"

def create_random_user(db: Session, *, password: str = "password", role: str = 'employee', organization_id: int = None) -> User:
    email = random_email()
    username = random_lower_string()
    full_name = random_lower_string().capitalize()
    user_in = UserCreate(username=username, email=email, password=password, role=UserRole(role), organization_id=organization_id, full_name=full_name)
    return crud_user.create(db=db, obj_in=user_in)

def authentication_token_from_username(
    *, client: TestClient, username: str, db: Session
) -> dict[str, str]:
    """
    Return a valid token headers for the user.
    """
    user = crud_user.get_by_username(db, username=username)
    password = user.username  # In tests, we can use a simple password convention
    
    # A bit of a hack to set a known password for login
    from app.core.security import get_password_hash
    user.hashed_password = get_password_hash(password)
    db.add(user)
    db.commit()

    login_data = {"username": username, "password": password}
    r = client.post(f"/api/v1/auth/token", data=login_data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
