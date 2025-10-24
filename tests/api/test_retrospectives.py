from datetime import date, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from tests.utils.user import create_random_user
from tests.utils.external_account import create_random_external_account
from app.models.external_account import AccountType


def test_generate_ai_retrospective_unauthorized(
    client: TestClient, db: Session
) -> None:
    request_data = {
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=1)).isoformat(),
    }
    response = client.post(f"{settings.API_V1_STR}/retrospectives/generate", json=request_data)
    assert response.status_code == 401


def test_generate_ai_retrospective_no_accounts(
    client: TestClient, db: Session
) -> None:
    user = create_random_user(db)
    from tests.utils.user import authentication_token_from_username
    user_token_headers = authentication_token_from_username(
        client=client, username=user.username, db=db
    )

    request_data = {
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=1)).isoformat(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/retrospectives/generate",
        headers=user_token_headers,
        json=request_data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "No external accounts linked" in content["content"]


def test_generate_ai_retrospective_with_accounts(
    client: TestClient, db: Session
) -> None:
    user = create_random_user(db)
    create_random_external_account(db, owner_id=user.id, account_type=AccountType.JIRA)
    
    from tests.utils.user import authentication_token_from_username
    user_token_headers = authentication_token_from_username(
        client=client, username=user.username, db=db
    )

    start_date = date(2025, 1, 1)
    end_date = date(2025, 6, 30)
    request_data = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/retrospectives/generate",
        headers=user_token_headers,
        json=request_data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "mock summary" in content["content"]
    assert "Mock activities for jira" in content["content"]
    assert "2025-01-01" in content["content"]
    assert "2025-06-30" in content["content"]
