from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import AccountType
from tests.utils.user import create_random_user, authentication_token_from_username

def test_create_external_account(client: TestClient, db: Session):
    user = create_random_user(db)
    headers = authentication_token_from_username(client=client, username=user.username, db=db)

    data = {
        "account_type": "jira",
        "username": "testuser@jira.com",
        "access_token": "a-super-secret-jira-token"
    }
    response = client.post("/api/v1/external-accounts/", headers=headers, json=data)
    
    assert response.status_code == 201
    created_account = response.json()
    assert created_account["account_type"] == "jira"
    assert created_account["username"] == "testuser@jira.com"
    assert "id" in created_account
    assert "access_token" not in created_account

def test_read_external_accounts(client: TestClient, db: Session):
    user = create_random_user(db)
    headers = authentication_token_from_username(client=client, username=user.username, db=db)
    data = {"account_type": "bitbucket", "username": "testuser@bitbucket.com", "access_token": "a-token"}
    client.post("/api/v1/external-accounts/", headers=headers, json=data)

    response = client.get("/api/v1/external-accounts/", headers=headers)
    assert response.status_code == 200
    accounts = response.json()
    assert len(accounts) == 1
    assert accounts[0]["account_type"] == "bitbucket"

def test_delete_external_account(client: TestClient, db: Session):
    user = create_random_user(db)
    headers = authentication_token_from_username(client=client, username=user.username, db=db)
    data = {"account_type": "jira", "username": "testuser@jira.com", "access_token": "a-token"}
    response = client.post("/api/v1/external-accounts/", headers=headers, json=data)
    account_id = response.json()["id"]

    response = client.delete(f"/api/v1/external-accounts/{account_id}", headers=headers)
    assert response.status_code == 200

    # Verify it's deleted
    response = client.get(f"/api/v1/external-accounts/", headers=headers)
    accounts = response.json()
    assert len(accounts) == 0

def test_delete_other_user_account_fails(client: TestClient, db: Session):
    # User A
    user_a = create_random_user(db)
    headers_a = authentication_token_from_username(client=client, username=user_a.username, db=db)
    data = {"account_type": "jira", "username": "user_a@jira.com", "access_token": "a-token"}
    response = client.post("/api/v1/external-accounts/", headers=headers_a, json=data)
    account_id = response.json()["id"]

    # User B
    user_b = create_random_user(db)
    headers_b = authentication_token_from_username(client=client, username=user_b.username, db=db)

    # User B tries to delete User A's account
    response = client.delete(f"/api/v1/external-accounts/{account_id}", headers=headers_b)
    assert response.status_code == 403 # Forbidden