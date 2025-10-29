from typing import List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.user import UserCreate
from tests.utils.user import create_random_user
from tests.utils.organization import create_random_organization
from tests.utils.project import create_random_project
from tests.utils.collaboration import create_random_interaction
from app.models.collaboration import InteractionType

def test_get_collaboration_network_data_by_project(
    client: TestClient, db: Session
) -> None:
    user1 = create_random_user(db)
    user2 = create_random_user(db)
    user3 = create_random_user(db)
    org = create_random_organization(db)
    pm = create_random_user(db, organization_id=org.id)
    project = create_random_project(db, pm_id=pm.id)

    create_random_interaction(db, source_user=user1, target_user=user2, project=project, type=InteractionType.JIRA_COMMENT)
    create_random_interaction(db, source_user=user2, target_user=user3, project=project, type=InteractionType.BITBUCKET_PR_REVIEW)

    user1_token_headers = client.post(
        f"{settings.API_V1_STR}/auth/token",
        data={"username": user1.username, "password": "password"},
    ).json()["access_token"]

    response = client.get(
        f"{settings.API_V1_STR}/collaborations/network-data?project_id={project.id}",
        headers={"Authorization": f"Bearer {user1_token_headers}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "graph" in data
    assert "analysis" in data
    assert len(data["graph"]["nodes"]) == 3
    assert len(data["graph"]["edges"]) == 2
    assert data["analysis"]["most_reviews"][0]["user_id"] == user2.id

def test_get_collaboration_network_data_by_organization(
    client: TestClient, db: Session
) -> None:
    user1 = create_random_user(db)
    org1 = create_random_organization(db)
    user1.organization_id = org1.id
    db.add(user1)

    user2 = create_random_user(db)
    org2 = create_random_organization(db, parent_id=org1.id)
    user2.organization_id = org2.id
    db.add(user2)
    
    user3 = create_random_user(db) # Belongs to a different org tree
    org3 = create_random_organization(db)
    user3.organization_id = org3.id
    db.add(user3)
    db.commit()

    pm = create_random_user(db, organization_id=org1.id)
    project = create_random_project(db, pm_id=pm.id)

    create_random_interaction(db, source_user=user1, target_user=user2, project=project, type=InteractionType.JIRA_MENTION)
    create_random_interaction(db, source_user=user1, target_user=user3, project=project, type=InteractionType.JIRA_MENTION)


    user1_token_headers = client.post(
        f"{settings.API_V1_STR}/auth/token",
        data={"username": user1.username, "password": "password"},
    ).json()["access_token"]

    response = client.get(
        f"{settings.API_V1_STR}/collaborations/network-data?organization_id={org1.id}",
        headers={"Authorization": f"Bearer {user1_token_headers}"},
    )
    assert response.status_code == 200
    data = response.json()
    # user1, user2, user3 should be in the graph as user1 interacted with them
    assert len(data["graph"]["nodes"]) == 3
    # user1 -> user2, user1 -> user3
    assert len(data["graph"]["edges"]) == 2
    assert data["analysis"]["most_help"][0]["user_id"] in [user2.id, user3.id]


def test_get_collaboration_network_data_no_filter_fails(
    client: TestClient, db: Session
) -> None:
    user = create_random_user(db)
    user_token_headers = client.post(
        f"{settings.API_V1_STR}/auth/token",
        data={"username": user.username, "password": "password"},
    ).json()["access_token"]

    response = client.get(
        f"{settings.API_V1_STR}/collaborations/network-data",
        headers={"Authorization": f"Bearer {user_token_headers}"},
    )
    assert response.status_code == 400
    assert "Either project_id or organization_id must be provided" in response.json()["detail"]

def test_get_collaboration_network_data_unauthenticated_fails(
    client: TestClient, db: Session
) -> None:
    response = client.get(f"{settings.API_V1_STR}/collaborations/network-data?project_id=1")
    assert response.status_code == 401