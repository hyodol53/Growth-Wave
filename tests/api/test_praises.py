from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from tests.utils.user import create_random_user, authentication_token_from_username


def test_create_praise(client: TestClient, db: Session):
    user_one = create_random_user(db)
    user_two = create_random_user(db)
    user_one_headers = authentication_token_from_username(
        client=client, username=user_one.username, db=db
    )

    # User one praises user two
    praise_data = {
        "recipient_id": user_two.id,
        "message": "Great job on the presentation!",
        "hashtags": ["#teamplayer", "#presentationskills"]
    }
    response = client.post("/api/v1/praises/", headers=user_one_headers, json=praise_data)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == praise_data["message"]
    assert "recipient_id" not in data # Recipient ID shouldn't be in the final praise response schema
    assert len(data["strengths"]) == 2
    found_hashtags = {s["hashtag"] for s in data["strengths"]}
    assert found_hashtags == {"#teamplayer", "#presentationskills"}


def test_praise_oneself_fails(client: TestClient, db: Session):
    user = create_random_user(db)
    user_headers = authentication_token_from_username(client=client, username=user.username, db=db)
    praise_data = {"recipient_id": user.id, "message": "I'm awesome", "hashtags": ["#awesome"]}
    response = client.post("/api/v1/praises/", headers=user_headers, json=praise_data)
    assert response.status_code == 400
    assert "You cannot praise yourself" in response.json()["detail"]


def test_praise_limit(client: TestClient, db: Session):
    user_one = create_random_user(db)
    user_two = create_random_user(db)
    user_one_headers = authentication_token_from_username(
        client=client, username=user_one.username, db=db
    )
    praise_data = {"recipient_id": user_two.id, "message": "praise", "hashtags": ["#test"]}

    # In praises.py, PRAISE_LIMIT_PER_PERIOD is 5
    for i in range(5):
        response = client.post("/api/v1/praises/", headers=user_one_headers, json=praise_data)
        assert response.status_code == 201, f"Failed on iteration {i+1}"

    # The 6th attempt should fail
    response = client.post("/api/v1/praises/", headers=user_one_headers, json=praise_data)
    assert response.status_code == 429


def test_read_praise_inbox(client: TestClient, db: Session):
    user_one = create_random_user(db)
    user_two = create_random_user(db)
    user_one_headers = authentication_token_from_username(client=client, username=user_one.username, db=db)
    user_two_headers = authentication_token_from_username(client=client, username=user_two.username, db=db)

    # User one praises user two
    client.post("/api/v1/praises/", headers=user_one_headers, json={
        "recipient_id": user_two.id, "message": "First praise", "hashtags": ["#1"]
    })
    # User one praises user two again
    client.post("/api/v1/praises/", headers=user_one_headers, json={
        "recipient_id": user_two.id, "message": "Second praise", "hashtags": ["#2"]
    })

    # Check user two's inbox
    response = client.get("/api/v1/praises/inbox/", headers=user_two_headers)
    assert response.status_code == 200
    inbox_data = response.json()
    assert len(inbox_data) == 2
    assert inbox_data[0]["message"] == "Second praise" # Most recent first

    # Check user one's inbox (should be empty)
    response = client.get("/api/v1/praises/inbox/", headers=user_one_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_read_strength_profile(client: TestClient, db: Session):
    user_one = create_random_user(db)
    user_two = create_random_user(db)
    user_three = create_random_user(db)
    user_one_headers = authentication_token_from_username(client=client, username=user_one.username, db=db)
    user_three_headers = authentication_token_from_username(client=client, username=user_three.username, db=db)

    # User 1 praises User 2
    client.post("/api/v1/praises/", headers=user_one_headers, json={
        "recipient_id": user_two.id, "message": "a", "hashtags": ["#helpful", "#smart"]
    })
    # User 3 praises User 2
    client.post("/api/v1/praises/", headers=user_three_headers, json={
        "recipient_id": user_two.id, "message": "b", "hashtags": ["#smart", "#leader"]
    })

    # Get User 2's strength profile
    response = client.get(f"/api/v1/praises/users/{user_two.id}/strength-profile/", headers=user_one_headers) # any authenticated user can see
    assert response.status_code == 200
    profile = response.json()
    assert profile["user_id"] == user_two.id
    assert profile["full_name"] == user_two.full_name
    
    strengths = profile["strengths"]
    assert len(strengths) == 3
    # Sorted by count desc, then hashtag asc
    assert strengths[0]["hashtag"] == "#smart"
    assert strengths[0]["count"] == 2
    assert strengths[1]["hashtag"] == "#helpful"
    assert strengths[1]["count"] == 1
    assert strengths[2]["hashtag"] == "#leader"
    assert strengths[2]["count"] == 1
