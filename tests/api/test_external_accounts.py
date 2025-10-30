from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.external_account import Provider
from tests.utils.user import create_random_user, authentication_token_from_username

def test_create_external_account(client: TestClient, db: Session) -> None:
    """
    Test creating an external account.
    """
    user = create_random_user(db)
    headers = authentication_token_from_username(client=client, username=user.username, db=db)
    
    data = {
        "provider": "jira",
        "account_id": "test@example.com",
        "credentials": "my-secret-jira-token"
    }
    response = client.post(f"{settings.API_V1_STR}/external-accounts", headers=headers, json=data)
    
    assert response.status_code == 201
    content = response.json()
    assert content["provider"] == "jira"
    assert content["account_id"] == "test@example.com"
    assert "credentials" not in content
    assert "id" in content

def test_read_external_accounts(client: TestClient, db: Session) -> None:
    """
    Test reading external accounts for the current user.
    """
    user = create_random_user(db)
    headers = authentication_token_from_username(client=client, username=user.username, db=db)
    
    # Create two accounts for the user
    client.post(f"{settings.API_V1_STR}/external-accounts", headers=headers, json={
        "provider": "jira", "account_id": "jira@test.com", "credentials": "token1"
    })
    client.post(f"{settings.API_V1_STR}/external-accounts", headers=headers, json={
        "provider": "bitbucket", "account_id": "bitbucket@test.com", "credentials": "token2"
    })
    
    response = client.get(f"{settings.API_V1_STR}/external-accounts", headers=headers)
    
    assert response.status_code == 200
    accounts = response.json()
    assert len(accounts) == 2
    assert accounts[0]["provider"] == "jira"
    assert accounts[1]["provider"] == "bitbucket"

def test_delete_external_account(client: TestClient, db: Session) -> None:
    """
    Test deleting an external account.
    """
    user = create_random_user(db)
    headers = authentication_token_from_username(client=client, username=user.username, db=db)
    
    # Create an account to delete
    creation_response = client.post(f"{settings.API_V1_STR}/external-accounts", headers=headers, json={
        "provider": "jira", "account_id": "to_delete@test.com", "credentials": "token"
    })
    account_id = creation_response.json()["id"]
    
    # Delete the account
    delete_response = client.delete(f"{settings.API_V1_STR}/external-accounts/{account_id}", headers=headers)
    assert delete_response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"{settings.API_V1_STR}/external-accounts", headers=headers)
    assert len(get_response.json()) == 0

def test_delete_other_user_account_fails(client: TestClient, db: Session) -> None:
    """
    Test that a user cannot delete another user's external account.
    """
    user1 = create_random_user(db)
    user2 = create_random_user(db)
    
    # User1 creates an account
    headers1 = authentication_token_from_username(client=client, username=user1.username, db=db)
    creation_response = client.post(f"{settings.API_V1_STR}/external-accounts", headers=headers1, json={
        "provider": "jira", "account_id": "user1_account@test.com", "credentials": "token"
    })
    account_id = creation_response.json()["id"]
    
    # User2 tries to delete it
    headers2 = authentication_token_from_username(client=client, username=user2.username, db=db)
    delete_response = client.delete(f"{settings.API_V1_STR}/external-accounts/{account_id}", headers=headers2)
    
    assert delete_response.status_code == 403 # Forbidden
