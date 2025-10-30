
import pytest
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.core.database import Base, get_db
from app.api.deps import get_current_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up the test database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db() -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    yield db
    db.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db) -> Generator:
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

from app.models.user import UserRole
from tests.utils.user import create_random_user, authentication_token_from_username

@pytest.fixture(scope="function")
def superuser_token_headers(client: TestClient, db: Session) -> dict:
    admin_user = create_random_user(db, role=UserRole.ADMIN)
    return authentication_token_from_username(client=client, username=admin_user.username, db=db)

@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db: Session) -> dict:
    user = create_random_user(db, role=UserRole.EMPLOYEE)
    return authentication_token_from_username(client=client, username=user.username, db=db)
