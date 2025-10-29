import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.schemas.evaluation import PeerEvaluationBase
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.project import create_random_project
from tests.utils.project_member import create_project_member
from tests.utils.evaluation import create_random_evaluation_period

def test_get_my_evaluation_tasks(client: TestClient, db: Session) -> None:
    # 1. Setup
    user1 = create_random_user(db)
    user2 = create_random_user(db)
    user1_headers = authentication_token_from_username(client=client, username=user1.username, db=db)

    # Create an active evaluation period
    today = datetime.date.today()
    create_random_evaluation_period(db, name="2025-H1", start_date=today, end_date=today + datetime.timedelta(days=30))

    # Create projects
    project1 = create_random_project(db, pm_id=user1.id, start_date=today, end_date=today + datetime.timedelta(days=10))
    project2 = create_random_project(db, pm_id=user2.id, start_date=today, end_date=today + datetime.timedelta(days=10))
    # Project outside the evaluation period
    project3 = create_random_project(db, pm_id=user1.id, start_date=today - datetime.timedelta(days=60), end_date=today - datetime.timedelta(days=30))

    create_project_member(db, project_id=project1.id, user_id=user1.id, is_pm=True)
    create_project_member(db, project_id=project2.id, user_id=user1.id, is_pm=False)
    create_project_member(db, project_id=project3.id, user_id=user1.id, is_pm=True)

    # 2. Action
    response = client.get("/api/v1/evaluations/my-tasks", headers=user1_headers)
    
    # 3. Assert
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    
    project_ids = {task["project_id"] for task in tasks}
    assert project1.id in project_ids
    assert project2.id in project_ids
    assert project3.id not in project_ids

    for task in tasks:
        if task["project_id"] == project1.id:
            assert task["user_role_in_project"] == "PM"
        if task["project_id"] == project2.id:
            assert task["user_role_in_project"] == "MEMBER"

def test_get_peer_evaluation_details(client: TestClient, db: Session) -> None:
    # 1. Setup
    evaluator = create_random_user(db)
    evaluatee1 = create_random_user(db)
    evaluatee2 = create_random_user(db)
    evaluator_headers = authentication_token_from_username(client=client, username=evaluator.username, db=db)

    today = datetime.date.today()
    create_random_evaluation_period(db, name="2025-H1", start_date=today, end_date=today + datetime.timedelta(days=30))
    
    project = create_random_project(db, pm_id=evaluator.id, start_date=today, end_date=today + datetime.timedelta(days=10))
    create_project_member(db, project_id=project.id, user_id=evaluator.id, is_pm=True)
    create_project_member(db, project_id=project.id, user_id=evaluatee1.id, is_pm=False)
    create_project_member(db, project_id=project.id, user_id=evaluatee2.id, is_pm=False)

    # 2. Action (Not started)
    response_not_started = client.get(f"/api/v1/evaluations/peer-evaluations/{project.id}", headers=evaluator_headers)
    
    # 3. Assert (Not started)
    assert response_not_started.status_code == 200
    details = response_not_started.json()
    assert details["project_id"] == project.id
    assert details["status"] == "NOT_STARTED"
    assert len(details["peers_to_evaluate"]) == 2
    assert details["peers_to_evaluate"][0]["score"] is None

    # 4. Action (In progress)
    # Evaluator evaluates evaluatee1
    evaluation_data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": evaluatee1.id, "score": 60, "comment": "Good"}
        ]
    }
    client.post("/api/v1/evaluations/peer-evaluations/", headers=evaluator_headers, json=evaluation_data)
    
    response_in_progress = client.get(f"/api/v1/evaluations/peer-evaluations/{project.id}", headers=evaluator_headers)
    
    # 5. Assert (In progress)
    assert response_in_progress.status_code == 200
    details_in_progress = response_in_progress.json()
    assert details_in_progress["status"] == "IN_PROGRESS"
    
    evaluated_peer = next(p for p in details_in_progress["peers_to_evaluate"] if p["evaluatee_id"] == evaluatee1.id)
    unevaluated_peer = next(p for p in details_in_progress["peers_to_evaluate"] if p["evaluatee_id"] == evaluatee2.id)
    
    assert evaluated_peer["score"] == 60
    assert evaluated_peer["comment"] == "Good"
    assert unevaluated_peer["score"] is None

def test_upsert_peer_evaluations(client: TestClient, db: Session) -> None:
    # 1. Setup
    evaluator = create_random_user(db)
    evaluatee = create_random_user(db)
    evaluator_headers = authentication_token_from_username(client=client, username=evaluator.username, db=db)

    today = datetime.date.today()
    create_random_evaluation_period(db, name="2025-H1", start_date=today, end_date=today + datetime.timedelta(days=30))
    
    project = create_random_project(db, pm_id=evaluator.id, start_date=today, end_date=today + datetime.timedelta(days=10))
    create_project_member(db, project_id=project.id, user_id=evaluator.id, is_pm=False)
    create_project_member(db, project_id=project.id, user_id=evaluatee.id, is_pm=False)

    # 2. Action (Create)
    create_data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": evaluatee.id, "score": 65, "comment": "Initial feedback"}
        ]
    }
    response_create = client.post("/api/v1/evaluations/peer-evaluations/", headers=evaluator_headers, json=create_data)
    
    # 3. Assert (Create)
    assert response_create.status_code == 200
    assert response_create.json()[0]["score"] == 65
    assert response_create.json()[0]["comment"] == "Initial feedback"

    # 4. Action (Update)
    update_data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": evaluatee.id, "score": 68, "comment": "Updated feedback"}
        ]
    }
    response_update = client.post("/api/v1/evaluations/peer-evaluations/", headers=evaluator_headers, json=update_data)

    # 5. Assert (Update)
    assert response_update.status_code == 200
    assert response_update.json()[0]["score"] == 68
    assert response_update.json()[0]["comment"] == "Updated feedback"

def test_upsert_pm_evaluations(client: TestClient, db: Session) -> None:
    # 1. Setup
    pm = create_random_user(db)
    member = create_random_user(db)
    pm_headers = authentication_token_from_username(client=client, username=pm.username, db=db)

    today = datetime.date.today()
    create_random_evaluation_period(db, name="2025-H1", start_date=today, end_date=today + datetime.timedelta(days=30))
    
    project = create_random_project(db, pm_id=pm.id, start_date=today, end_date=today + datetime.timedelta(days=10))
    create_project_member(db, project_id=project.id, user_id=pm.id, is_pm=True)
    create_project_member(db, project_id=project.id, user_id=member.id, is_pm=False)

    # 2. Action (Create)
    create_data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": member.id, "score": 80, "comment": "Good progress"}
        ]
    }
    response_create = client.post("/api/v1/evaluations/pm-evaluations/", headers=pm_headers, json=create_data)
    
    # 3. Assert (Create)
    assert response_create.status_code == 200
    assert response_create.json()[0]["score"] == 80
    assert response_create.json()[0]["comment"] == "Good progress"

    # 4. Action (Update)
    update_data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": member.id, "score": 85, "comment": "Excellent progress"}
        ]
    }
    response_update = client.post("/api/v1/evaluations/pm-evaluations/", headers=pm_headers, json=update_data)

    # 5. Assert (Update)
    assert response_update.status_code == 200
    assert response_update.json()[0]["score"] == 85
    assert response_update.json()[0]["comment"] == "Excellent progress"
