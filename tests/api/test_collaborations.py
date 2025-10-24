from typing import List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.config import settings
from app.schemas.collaboration import CollaborationInteractionCreate
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.project import create_random_project
from tests.utils.organization import create_random_organization

def test_collect_collaboration_data_superuser(
    client: TestClient, db: Session
) -> None:
    admin = create_random_user(db, role='admin')
    superuser_token_headers = authentication_token_from_username(
        client=client, username=admin.username, db=db
    )
    org = create_random_organization(db)
    user1 = create_random_user(db, organization_id=org.id)
    user2 = create_random_user(db, organization_id=org.id)
    project = create_random_project(db, owner_org_id=org.id)

    interaction_data: List[CollaborationInteractionCreate] = [
        CollaborationInteractionCreate(
            source_user_id=user1.id,
            target_user_id=user2.id,
            project_id=project.id,
            interaction_type="jira_comment",
            occurred_at=datetime.utcnow(),
        )
    ]
    
    # Pydantic v2 requires model_dump_json for TestClient
    json_data = [item.model_dump_json() for item in interaction_data]
    # The client expects a list of dicts, not a list of json strings
    import json
    dict_data = [json.loads(item) for item in json_data]


    response = client.post(
        f"{settings.API_V1_STR}/collaborations/collect",
        headers=superuser_token_headers,
        json=dict_data,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert content[0]["source_user_id"] == user1.id
    assert content[0]["target_user_id"] == user2.id
    assert content[0]["project_id"] == project.id
    assert content[0]["interaction_type"] == "jira_comment"

def test_collect_collaboration_data_normal_user(
    client: TestClient, db: Session
) -> None:
    # Create a normal user and get their token
    org = create_random_organization(db)
    user = create_random_user(db, organization_id=org.id)
    user_token_headers = authentication_token_from_username(
        client=client, username=user.username, db=db
    )


    interaction_data: List[CollaborationInteractionCreate] = [
        CollaborationInteractionCreate(
            source_user_id=user.id,
            target_user_id=user.id, # Dummy data
            project_id=1, # Dummy data
            interaction_type="jira_comment",
            occurred_at=datetime.utcnow(),
        )
    ]
    import json
    json_data = [item.model_dump_json() for item in interaction_data]
    dict_data = [json.loads(item) for item in json_data]

    response = client.post(
        f"{settings.API_V1_STR}/collaborations/collect",
        headers=user_token_headers,
        json=dict_data,
    )
    assert response.status_code == 403
