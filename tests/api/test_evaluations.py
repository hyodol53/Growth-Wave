from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.user import create_random_user, authentication_token_from_username

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
