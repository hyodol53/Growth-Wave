from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.project import create_random_project, add_user_to_project
import datetime

def test_create_evaluation_weight_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)
    
    data = {"role": "employee", "item": "peer_review", "weight": 0.4}
    response = client.post("/api/v1/evaluations/", headers=superuser_token_headers, json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["role"] == data["role"]
    assert content["item"] == data["item"]
    assert content["weight"] == data["weight"]

def test_create_evaluation_weight_normal_user(client: TestClient, db: Session) -> None:
    normal_user = create_random_user(db, role="employee")
    normal_user_token_headers = authentication_token_from_username(client=client, username=normal_user.username, db=db)

    data = {"role": "employee", "item": "pm_review", "weight": 0.6}
    response = client.post("/api/v1/evaluations/", headers=normal_user_token_headers, json=data)
    assert response.status_code == 403

def test_read_evaluation_weights_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    response = client.get("/api/v1/evaluations/", headers=superuser_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)

def test_read_evaluation_weights_normal_user(client: TestClient, db: Session) -> None:
    normal_user = create_random_user(db, role="employee")
    normal_user_token_headers = authentication_token_from_username(client=client, username=normal_user.username, db=db)

    response = client.get("/api/v1/evaluations/", headers=normal_user_token_headers)
    assert response.status_code == 403

def test_update_evaluation_weight_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    # First create one
    create_data = {"role": "team_lead", "item": "qualitative_review", "weight": 0.7}
    response = client.post("/api/v1/evaluations/", headers=superuser_token_headers, json=create_data)
    assert response.status_code == 200
    created_id = response.json()["id"]

    # Now update it
    update_data = {"role": "team_lead", "item": "qualitative_review", "weight": 0.8}
    response = client.put(f"/api/v1/evaluations/{created_id}", headers=superuser_token_headers, json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["weight"] == update_data["weight"]

def test_delete_evaluation_weight_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    # First create one
    create_data = {"role": "dept_head", "item": "peer_review", "weight": 0.2}
    response = client.post("/api/v1/evaluations/", headers=superuser_token_headers, json=create_data)
    assert response.status_code == 200
    created_id = response.json()["id"]

    # Now delete it
    response = client.delete(f"/api/v1/evaluations/{created_id}", headers=superuser_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == created_id

    # Verify it's gone by listing all and checking it's not there.
    list_response = client.get("/api/v1/evaluations/", headers=superuser_token_headers)
    assert created_id not in [item['id'] for item in list_response.json()]


def test_create_evaluation_period_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    data = {"name": "2025-H1", "start_date": datetime.date(2025, 1, 1).isoformat(), "end_date": datetime.date(2025, 6, 30).isoformat()}
    response = client.post("/api/v1/evaluations/evaluation-periods/", headers=superuser_token_headers, json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["start_date"] == data["start_date"]
    assert content["end_date"] == data["end_date"]

def test_create_evaluation_period_normal_user(client: TestClient, db: Session) -> None:
    normal_user = create_random_user(db, role="employee")
    normal_user_token_headers = authentication_token_from_username(client=client, username=normal_user.username, db=db)

    data = {"name": "2025-H2", "start_date": datetime.date(2025, 7, 1).isoformat(), "end_date": datetime.date(2025, 12, 31).isoformat()}
    response = client.post("/api/v1/evaluations/evaluation-periods/", headers=normal_user_token_headers, json=data)
    assert response.status_code == 403

def test_read_evaluation_periods_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    response = client.get("/api/v1/evaluations/evaluation-periods/", headers=superuser_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)

def test_read_evaluation_periods_normal_user(client: TestClient, db: Session) -> None:
    normal_user = create_random_user(db, role="employee")
    normal_user_token_headers = authentication_token_from_username(client=client, username=normal_user.username, db=db)

    response = client.get("/api/v1/evaluations/evaluation-periods/", headers=normal_user_token_headers)
    assert response.status_code == 403

def test_update_evaluation_period_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    # First create one
    create_data = {"name": "2026-H1", "start_date": datetime.date(2026, 1, 1).isoformat(), "end_date": datetime.date(2026, 6, 30).isoformat()}
    response = client.post("/api/v1/evaluations/evaluation-periods/", headers=superuser_token_headers, json=create_data)
    assert response.status_code == 200
    created_id = response.json()["id"]

    # Now update it
    update_data = {"name": "2026-H1-Updated", "start_date": datetime.date(2026, 1, 1).isoformat(), "end_date": datetime.date(2026, 7, 15).isoformat()}
    response = client.put(f"/api/v1/evaluations/evaluation-periods/{created_id}", headers=superuser_token_headers, json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == update_data["name"]
    assert content["end_date"] == update_data["end_date"]

def test_delete_evaluation_period_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    # First create one
    create_data = {"name": "2027-H1", "start_date": datetime.date(2027, 1, 1).isoformat(), "end_date": datetime.date(2027, 6, 30).isoformat()}
    response = client.post("/api/v1/evaluations/evaluation-periods/", headers=superuser_token_headers, json=create_data)
    assert response.status_code == 200
    created_id = response.json()["id"]

    # Now delete it
    response = client.delete(f"/api/v1/evaluations/evaluation-periods/{created_id}", headers=superuser_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == created_id

    # Verify it's gone by listing all and checking it's not there.
    list_response = client.get("/api/v1/evaluations/evaluation-periods/", headers=superuser_token_headers)
    assert created_id not in [item['id'] for item in list_response.json()]


def test_create_department_grade_ratio_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    data = {"department_grade": "S", "s_ratio": 0.6, "a_ratio": 0.4}
    response = client.post("/api/v1/evaluations/department-grade-ratios/", headers=superuser_token_headers, json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["department_grade"] == data["department_grade"]
    assert content["s_ratio"] == data["s_ratio"]
    assert content["a_ratio"] == data["a_ratio"]

def test_create_department_grade_ratio_normal_user(client: TestClient, db: Session) -> None:
    normal_user = create_random_user(db, role="employee")
    normal_user_token_headers = authentication_token_from_username(client=client, username=normal_user.username, db=db)

    data = {"department_grade": "A", "s_ratio": 0.4, "a_ratio": 0.6}
    response = client.post("/api/v1/evaluations/department-grade-ratios/", headers=normal_user_token_headers, json=data)
    assert response.status_code == 403

def test_read_department_grade_ratios_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    response = client.get("/api/v1/evaluations/department-grade-ratios/", headers=superuser_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)

def test_read_department_grade_ratios_normal_user(client: TestClient, db: Session) -> None:
    normal_user = create_random_user(db, role="employee")
    normal_user_token_headers = authentication_token_from_username(client=client, username=normal_user.username, db=db)

    response = client.get("/api/v1/evaluations/department-grade-ratios/", headers=normal_user_token_headers)
    assert response.status_code == 403

def test_update_department_grade_ratio_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    # First create one
    create_data = {"department_grade": "B", "s_ratio": 0.2, "a_ratio": 0.4}
    response = client.post("/api/v1/evaluations/department-grade-ratios/", headers=superuser_token_headers, json=create_data)
    assert response.status_code == 200
    created_id = response.json()["id"]

    # Now update it
    update_data = {"department_grade": "B", "s_ratio": 0.25, "a_ratio": 0.35}
    response = client.put(f"/api/v1/evaluations/department-grade-ratios/{created_id}", headers=superuser_token_headers, json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["s_ratio"] == update_data["s_ratio"]
    assert content["a_ratio"] == update_data["a_ratio"]

def test_delete_department_grade_ratio_superuser(client: TestClient, db: Session) -> None:
    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    # First create one
    create_data = {"department_grade": "C", "s_ratio": 0.0, "a_ratio": 0.2}
    response = client.post("/api/v1/evaluations/department-grade-ratios/", headers=superuser_token_headers, json=create_data)
    assert response.status_code == 200
    created_id = response.json()["id"]

    # Now delete it
    response = client.delete(f"/api/v1/evaluations/department-grade-ratios/{created_id}", headers=superuser_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == created_id

    # Verify it's gone by listing all and checking it's not there.
    list_response = client.get("/api/v1/evaluations/department-grade-ratios/", headers=superuser_token_headers)
    assert created_id not in [item['id'] for item in list_response.json()]

def test_create_or_update_peer_evaluations(client: TestClient, db: Session) -> None:
    # 1. Setup: Create users, project, evaluation period
    evaluator = create_random_user(db, role="employee")
    evaluatee1 = create_random_user(db, role="employee")
    evaluatee2 = create_random_user(db, role="employee")
    pm_user = create_random_user(db, role="team_lead")
    project = create_random_project(db, pm_id=pm_user.id)
    add_user_to_project(db, user_id=evaluator.id, project_id=project.id)
    add_user_to_project(db, user_id=evaluatee1.id, project_id=project.id)
    add_user_to_project(db, user_id=evaluatee2.id, project_id=project.id)

    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)
    today = datetime.date.today()
    # Make sure the active period covers the current date
    period_data = {"name": f"{today.year}-H{1 if today.month <= 6 else 2}", "start_date": (today - datetime.timedelta(days=1)).isoformat(), "end_date": (today + datetime.timedelta(days=1)).isoformat()}
    client.post("/api/v1/evaluations/evaluation-periods/", headers=superuser_token_headers, json=period_data)

    evaluator_token_headers = authentication_token_from_username(client=client, username=evaluator.username, db=db)

    # 2. Test valid peer evaluation submission
    valid_data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": evaluatee1.id, "scores": [10, 10, 5, 5, 5, 5, 10], "comment": "Good work"},
            {"project_id": project.id, "evaluatee_id": evaluatee2.id, "scores": [15, 15, 7, 7, 7, 7, 12], "comment": "Excellent"}
        ]
    }
    # Average score is (50 + 70) / 2 = 60 <= 70. This is valid.
    response = client.post("/api/v1/evaluations/peer-evaluations/", headers=evaluator_token_headers, json=valid_data)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2
    assert content[0]["evaluatee_id"] == evaluatee1.id
    assert content[0]["scores"][0] == 10
    assert sum(content[0]["scores"]) == 50

    # 3. Test invalid: incorrect number of scores
    invalid_scores_data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": evaluatee1.id, "scores": [10, 10, 5, 5, 5], "comment": "Wrong scores"}
        ]
    }
    response = client.post("/api/v1/evaluations/peer-evaluations/", headers=evaluator_token_headers, json=invalid_scores_data)
    assert response.status_code == 400
    assert "must have exactly 7 scores" in response.json()["detail"]

    # 4. Test invalid: score out of range
    out_of_range_data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": evaluatee1.id, "scores": [25, 10, 5, 5, 5, 5, 10], "comment": "Score too high"}
        ]
    }
    response = client.post("/api/v1/evaluations/peer-evaluations/", headers=evaluator_token_headers, json=out_of_range_data)
    assert response.status_code == 400
    assert "is out of range" in response.json()["detail"]

    # 5. Test invalid: average score > 70
    high_average_data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": evaluatee1.id, "scores": [20, 20, 10, 10, 10, 10, 20]}, # 100
            {"project_id": project.id, "evaluatee_id": evaluatee2.id, "scores": [10, 10, 5, 5, 5, 5, 10]}  # 50
        ]
    } # Average is 75 > 70
    response = client.post("/api/v1/evaluations/peer-evaluations/", headers=evaluator_token_headers, json=high_average_data)
    assert response.status_code == 400
    assert "Average score cannot exceed 70" in response.json()["detail"]

    # 6. Test UPSERT functionality
    upsert_data = {
        "evaluations": [
            {"project_id": project.id, "evaluatee_id": evaluatee1.id, "scores": [5, 5, 2, 2, 2, 2, 5], "comment": "Updated comment"}
        ]
    } # Total score 23
    response = client.post("/api/v1/evaluations/peer-evaluations/", headers=evaluator_token_headers, json=upsert_data)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert content[0]["evaluatee_id"] == evaluatee1.id
    assert content[0]["scores"][0] == 5
    assert content[0]["comment"] == "Updated comment"
    assert sum(content[0]["scores"]) == 23

def test_create_qualitative_evaluations(client: TestClient, db: Session) -> None:
    # 1. Setup: Create users, org, and evaluation period
    from tests.utils.organization import create_random_organization
    org = create_random_organization(db)
    team_lead = create_random_user(db, role="team_lead", organization_id=org.id)
    subordinate = create_random_user(db, role="employee", organization_id=org.id)

    admin_user = create_random_user(db, role="admin")
    superuser_token_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)
    today = datetime.date.today()
    period_data = {"name": f"{today.year}-H{1 if today.month <= 6 else 2}", "start_date": (today - datetime.timedelta(days=1)).isoformat(), "end_date": (today + datetime.timedelta(days=1)).isoformat()}
    client.post("/api/v1/evaluations/evaluation-periods/", headers=superuser_token_headers, json=period_data)

    team_lead_token_headers = authentication_token_from_username(client=client, username=team_lead.username, db=db)

    # 2. Test valid qualitative evaluation submission
    valid_data = {
        "evaluations": [
            {
                "evaluatee_id": subordinate.id,
                "qualitative_score": 18,
                "department_contribution_score": 9,
                "feedback": "Excellent contribution to the department goals."
            }
        ]
    }
    response = client.post("/api/v1/evaluations/qualitative-evaluations/", headers=team_lead_token_headers, json=valid_data)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert content[0]["evaluatee_id"] == subordinate.id
    assert content[0]["qualitative_score"] == 18
    assert content[0]["department_contribution_score"] == 9
    assert content[0]["feedback"] == "Excellent contribution to the department goals."

    # 3. Test invalid: score out of range
    invalid_score_data = {
        "evaluations": [
            {
                "evaluatee_id": subordinate.id,
                "qualitative_score": 25,  # Invalid score
                "department_contribution_score": 5,
                "feedback": "This should fail."
            }
        ]
    }
    response = client.post("/api/v1/evaluations/qualitative-evaluations/", headers=team_lead_token_headers, json=invalid_score_data)
    assert response.status_code == 422 # Pydantic validation error
    assert "Input should be less than or equal to 20" in response.json()["detail"][0]["msg"]