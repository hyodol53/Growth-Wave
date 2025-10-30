import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app import crud
from tests.utils.user import create_random_user, authentication_token_from_username

def test_create_retrospective(client: TestClient, db: Session) -> None:
    """
    Test creating a retrospective.
    """
    user = create_random_user(db)
    headers = authentication_token_from_username(client=client, username=user.username, db=db)
    
    data = {"title": "My First Retrospective", "content": "This was a good period."}
    response = client.post(f"{settings.API_V1_STR}/retrospectives", headers=headers, json=data)
    
    assert response.status_code == 201
    content = response.json()
    assert content["title"] == data["title"]
    assert content["content"] == data["content"]
    assert content["user_id"] == user.id

def test_read_user_retrospectives(client: TestClient, db: Session) -> None:
    """
    Test reading a user's own retrospectives.
    """
    user = create_random_user(db)
    headers = authentication_token_from_username(client=client, username=user.username, db=db)
    
    # Create two retrospectives for the user
    client.post(f"{settings.API_V1_STR}/retrospectives", headers=headers, json={"title": "Retro 1", "content": "Content 1"})
    client.post(f"{settings.API_V1_STR}/retrospectives", headers=headers, json={"title": "Retro 2", "content": "Content 2"})
    
    response = client.get(f"{settings.API_V1_STR}/retrospectives", headers=headers)
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    assert items[0]["title"] == "Retro 2" # Ordered by desc ID
    assert items[1]["title"] == "Retro 1"

def test_read_other_user_retrospective_fails(client: TestClient, db: Session) -> None:
    """
    Test that a user cannot read another user's retrospective.
    """
    user1 = create_random_user(db)
    user2 = create_random_user(db)
    headers1 = authentication_token_from_username(client=client, username=user1.username, db=db)
    headers2 = authentication_token_from_username(client=client, username=user2.username, db=db)

    # User 1 creates a retrospective
    create_resp = client.post(f"{settings.API_V1_STR}/retrospectives", headers=headers1, json={"title": "User1 Retro", "content": "secret"})
    retro_id = create_resp.json()["id"]

    # User 2 tries to read it
    response = client.get(f"{settings.API_V1_STR}/retrospectives/{retro_id}", headers=headers2)
    assert response.status_code == 404 # Because the query includes user_id, it's not found for user2

def test_update_retrospective(client: TestClient, db: Session) -> None:
    """
    Test updating a user's own retrospective.
    """
    user = create_random_user(db)
    headers = authentication_token_from_username(client=client, username=user.username, db=db)
    
    create_resp = client.post(f"{settings.API_V1_STR}/retrospectives", headers=headers, json={"title": "Original Title", "content": "Original Content"})
    retro_id = create_resp.json()["id"]
    
    update_data = {"title": "Updated Title"}
    response = client.put(f"{settings.API_V1_STR}/retrospectives/{retro_id}", headers=headers, json=update_data)
    
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == "Updated Title"
    assert content["content"] == "Original Content" # Content should remain unchanged

def test_delete_retrospective(client: TestClient, db: Session) -> None:
    """
    Test deleting a user's own retrospective.
    """
    user = create_random_user(db)
    headers = authentication_token_from_username(client=client, username=user.username, db=db)
    
    create_resp = client.post(f"{settings.API_V1_STR}/retrospectives", headers=headers, json={"title": "To Be Deleted", "content": "..."})
    retro_id = create_resp.json()["id"]
    
    delete_resp = client.delete(f"{settings.API_V1_STR}/retrospectives/{retro_id}", headers=headers)
    assert delete_resp.status_code == 204
    
    # Verify it's gone
    get_resp = client.get(f"{settings.API_V1_STR}/retrospectives/{retro_id}", headers=headers)
    assert get_resp.status_code == 404

def test_generate_retrospective_draft(client: TestClient, db: Session, monkeypatch) -> None:
    """
    Test the AI draft generation endpoint, mocking the external LLM call.
    """
    # Mock the LLM function to avoid actual API calls
    mock_draft = "This is a mock AI-generated retrospective draft."
    def mock_generate(*args, **kwargs):
        return mock_draft
        
    monkeypatch.setattr("app.services.retrospective_generator.generate_retrospective_from_gemini", mock_generate)
    
    user = create_random_user(db)
    headers = authentication_token_from_username(client=client, username=user.username, db=db)
    
    response = client.post(f"{settings.API_V1_STR}/retrospectives/generate", headers=headers)
    
    assert response.status_code == 200
    content = response.json()
    assert content["content"] == mock_draft