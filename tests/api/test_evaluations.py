from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.user import create_random_user, authentication_token_from_username
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
