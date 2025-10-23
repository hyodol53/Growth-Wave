import json
import io
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.user import create_random_user, authentication_token_from_username

def test_create_organization_by_admin(client: TestClient, db: Session):
    admin = create_random_user(db, role='admin')
    admin_token_headers = authentication_token_from_username(
        client=client, username=admin.username, db=db
    )
    
    org_data = {"name": "Test Department", "level": 2, "parent_id": None}
    response = client.post(
        "/api/v1/organizations/",
        headers=admin_token_headers,
        json=org_data,
    )
    assert response.status_code == 201
    created_org = response.json()
    assert created_org["name"] == org_data["name"]

def test_read_organizations_by_any_user(client: TestClient, db: Session):
    user = create_random_user(db, role='employee')
    user_token_headers = authentication_token_from_username(
        client=client, username=user.username, db=db
    )

    response = client.get("/api/v1/organizations/", headers=user_token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_upload_organizations_by_admin(client: TestClient, db: Session):
    # 1. Create admin user and get token
    admin = create_random_user(db, role='admin')
    admin_token_headers = authentication_token_from_username(
        client=client, username=admin.username, db=db
    )

    # 2. Prepare initial data in DB
    client.post("/api/v1/organizations/", headers=admin_token_headers, json={"name": "Old Department", "level": 1})

    # 3. Prepare file for upload with parent-child relationship
    org_data = [
        {"name": "New Center", "level": 1, "parent_name": None},
        {"name": "New Team", "level": 2, "parent_name": "New Center"}
    ]
    json_string = json.dumps(org_data)
    json_content = io.BytesIO(json_string.encode('utf-8'))
    
    # 4. Upload the file
    response = client.post(
        "/api/v1/organizations/upload",
        headers=admin_token_headers,
        files={"file": ("org_chart.json", json_content, "application/json")}
    )

    # 5. Assert response
    assert response.status_code == 200
    result = response.json()
    assert result["created"] == 2
    assert result["updated"] == 0
    assert result["deleted"] == 1 # "Old Department" should be deleted

    # 6. Verify DB state and parent-child relationship
    response = client.get("/api/v1/organizations/", headers=admin_token_headers)
    orgs = {org['name']: org for org in response.json()}
    assert len(orgs) == 2
    assert "New Center" in orgs
    assert "New Team" in orgs
    assert "Old Department" not in orgs

    center = orgs["New Center"]
    team = orgs["New Team"]
    assert team["parent_id"] == center["id"]
