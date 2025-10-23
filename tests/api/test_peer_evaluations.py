from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from tests.utils.user import create_random_user
from tests.utils.project import create_random_project
from tests.utils.project_member import create_project_member

def test_create_peer_evaluations_success(client: TestClient, db: Session) -> None:
    user1 = create_random_user(db, password="password")
    user2 = create_random_user(db)
    user3 = create_random_user(db)
    project = create_random_project(db)
    create_project_member(db, project_id=project.id, user_id=user1.id)
    create_project_member(db, project_id=project.id, user_id=user2.id)
    create_project_member(db, project_id=project.id, user_id=user3.id)

    login_data = {
        "username": user1.username,
        "password": "password"
    }
    r = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": user2.id, "score": 60, "feedback": "Good teamwork!"},
            {"project_id": project.id, "evaluatee_id": user3.id, "score": 80, "feedback": "Very helpful."},
        ]
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/peer-evaluations/", headers=headers, json=data)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2
    assert content[0]["score"] == 60
    assert content[0]["feedback"] == "Good teamwork!"
    assert content[1]["score"] == 80
    assert content[1]["feedback"] == "Very helpful."

def test_create_peer_evaluations_avg_score_too_high(client: TestClient, db: Session) -> None:
    user1 = create_random_user(db, password="password")
    user2 = create_random_user(db)
    user3 = create_random_user(db)
    project = create_random_project(db)
    create_project_member(db, project_id=project.id, user_id=user1.id)
    create_project_member(db, project_id=project.id, user_id=user2.id)
    create_project_member(db, project_id=project.id, user_id=user3.id)

    login_data = {
        "username": user1.username,
        "password": "password"
    }
    r = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": user2.id, "score": 71},
            {"project_id": project.id, "evaluatee_id": user3.id, "score": 71},
        ]
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/peer-evaluations/", headers=headers, json=data)
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Average score cannot exceed 70."

def test_create_peer_evaluations_unauthenticated(client: TestClient, db: Session) -> None:
    user2 = create_random_user(db)
    user3 = create_random_user(db)
    project = create_random_project(db)

    data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": user2.id, "score": 60},
            {"project_id": project.id, "evaluatee_id": user3.id, "score": 80},
        ]
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/peer-evaluations/", json=data)
    assert response.status_code == 401
