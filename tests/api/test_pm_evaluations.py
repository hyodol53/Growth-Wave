from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
import datetime
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.project import create_random_project
from tests.utils.project_member import create_project_member
from tests.utils.organization import create_random_organization
from tests.utils.evaluation import create_random_evaluation_period
from app.models.user import UserRole

def test_create_pm_evaluations_success(client: TestClient, db: Session) -> None:
    pm_user = create_random_user(db, password="password")
    member_user = create_random_user(db)
    org = create_random_organization(db)
    project = create_random_project(db, pm_id=pm_user.id)
    create_project_member(db, project_id=project.id, user_id=pm_user.id, is_pm=True)
    create_project_member(db, project_id=project.id, user_id=member_user.id)

    login_data = {
        "username": pm_user.username,
        "password": "password"
    }
    r = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": member_user.id, "score": 95}
        ]
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/pm-evaluations/", headers=headers, json=data)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert content[0]["score"] == 95
    assert content[0]["evaluator_id"] == pm_user.id

def test_create_pm_evaluations_not_a_pm(client: TestClient, db: Session) -> None:
    non_pm_user = create_random_user(db, password="password")
    member_user = create_random_user(db)
    org = create_random_organization(db)
    pm = create_random_user(db)
    project = create_random_project(db, pm_id=pm.id)
    create_project_member(db, project_id=project.id, user_id=non_pm_user.id, is_pm=False)
    create_project_member(db, project_id=project.id, user_id=member_user.id)

    login_data = {
        "username": non_pm_user.username,
        "password": "password"
    }
    r = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": member_user.id, "score": 95}
        ]
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/pm-evaluations/", headers=headers, json=data)
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == f"User is not a Project Manager for project {project.id}."

def test_create_pm_evaluations_score_out_of_range(client: TestClient, db: Session) -> None:
    pm_user = create_random_user(db, password="password")
    member_user = create_random_user(db)
    org = create_random_organization(db)
    project = create_random_project(db, pm_id=pm_user.id)
    create_project_member(db, project_id=project.id, user_id=pm_user.id, is_pm=True)
    create_project_member(db, project_id=project.id, user_id=member_user.id)

    login_data = {
        "username": pm_user.username,
        "password": "password"
    }
    r = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": member_user.id, "score": 101}
        ]
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/pm-evaluations/", headers=headers, json=data)
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Score must be between 0 and 100."

def test_create_pm_self_evaluation_as_admin(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role=UserRole.ADMIN, password="password")
    pm_user = create_random_user(db, role=UserRole.TEAM_LEAD)
    org = create_random_organization(db)
    project = create_random_project(db, pm_id=pm_user.id) # PM needs a project context
    headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    data = {"project_id": project.id, "evaluatee_id": pm_user.id, "score": 98}
    response = client.post(f"{settings.API_V1_STR}/evaluations/pm-self-evaluation/", headers=headers, json=data)
    
    assert response.status_code == 200
    content = response.json()
    assert content["score"] == 98
    assert content["evaluator_id"] == admin_user.id
    assert content["evaluatee_id"] == pm_user.id

def test_create_pm_self_evaluation_not_admin(client: TestClient, db: Session) -> None:
    normal_user = create_random_user(db, password="password")
    pm_user = create_random_user(db, role=UserRole.TEAM_LEAD)
    org = create_random_organization(db)
    project = create_random_project(db, pm_id=pm_user.id)
    headers = authentication_token_from_username(client=client, username=normal_user.username, db=db)

    data = {"project_id": project.id, "evaluatee_id": pm_user.id, "score": 98}
    response = client.post(f"{settings.API_V1_STR}/evaluations/pm-self-evaluation/", headers=headers, json=data)
    
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "The user doesn't have enough privileges"