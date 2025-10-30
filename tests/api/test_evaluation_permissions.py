from typing import List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import datetime

from app import crud
from app.core.config import settings
from app.models.user import User, UserRole
from app.schemas.project import ProjectCreate
from app.schemas.project_member import ProjectMemberCreate
from app.schemas.evaluation import (
    FinalEvaluationCreate,
    PmEvaluationBase,
    PeerEvaluationBase,
)
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.organization import create_random_organization
from tests.utils.project import create_random_project
from tests.utils.project_member import create_project_member
from tests.utils.utils import random_lower_string


def test_read_my_evaluation_result(
    client: TestClient, db: Session
) -> None:
    # Create users: one employee, one PM
    employee = create_random_user(db, role=UserRole.EMPLOYEE)
    pm = create_random_user(db, role=UserRole.TEAM_LEAD)
    
    # Create organization and project, assigning the PM
    org = create_random_organization(db)
    project_in = ProjectCreate(name=random_lower_string(), pm_id=pm.id)
    project = crud.project.project.create(db, obj_in=project_in)
    
    # Add users to project
    create_project_member(db, project_id=project.id, user_id=employee.id, is_pm=False)
    create_project_member(db, project_id=project.id, user_id=pm.id, is_pm=True)

    # Create evaluation data
    today = datetime.date.today()
    period = f"{today.year}-H{1 if today.month <= 6 else 2}"

    crud.final_evaluation.create(
        db,
        obj_in=FinalEvaluationCreate(
            evaluatee_id=employee.id,
            evaluation_period=period,
            final_score=88.5,
            grade="A",
        ),
    )
    crud.pm_evaluation.pm_evaluation.create(
        db,
        obj_in=PmEvaluationBase(
            project_id=project.id, evaluatee_id=employee.id, score=90
        ),
        evaluator_id=pm.id,
        evaluation_period=period,
    )

    # Get token and make request
    user_token_headers = authentication_token_from_username(
        client=client, username=employee.username, db=db
    )
    response = client.get(f"{settings.API_V1_STR}/evaluations/me", headers=user_token_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["evaluation_period"] == period
    assert data["grade"] == "A"
    assert len(data["pm_scores"]) == 1
    assert data["pm_scores"][0]["project_name"] == project.name
    assert data["pm_scores"][0]["pm_name"] == pm.full_name
    assert data["pm_scores"][0]["score"] == 90

    # FR-A-5.2: Ensure sensitive data is not exposed
    assert "final_score" not in data
    assert "peer_score" not in data
    assert "qualitative_score" not in data
    assert "final_evaluation" not in data


def test_read_subordinate_evaluation_as_dept_head(
    client: TestClient, db: Session
) -> None:
    # Create a specific organization for this test
    org = create_random_organization(db)
    # Create users: one dept_head, one subordinate within the same organization
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org.id)
    subordinate = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=org.id)

    # Create evaluation data
    today = datetime.date.today()
    period = f"{today.year}-H{1 if today.month <= 6 else 2}"
    
    crud.final_evaluation.create(
        db,
        obj_in=FinalEvaluationCreate(
            evaluatee_id=subordinate.id,
            evaluation_period=period,
            final_score=95.0,
            peer_score=92.0,
            pm_score=96.0,
            qualitative_score=97.0,
            grade="S",
        ),
    )
    # Create peer feedback
    peer = create_random_user(db)
    crud.peer_evaluation.peer_evaluation.upsert_multi(
        db,
        evaluations=[
            PeerEvaluationBase(project_id=1, evaluatee_id=subordinate.id, scores=[20, 20, 10, 10, 10, 5, 5], comment="Great team player!")
        ],
        evaluator_id=peer.id,
        evaluation_period=period,
    )

    # Get token and make request
    dept_head_token_headers = authentication_token_from_username(
        client=client, username=dept_head.username, db=db
    )
    response = client.get(
        f"{settings.API_V1_STR}/evaluations/{subordinate.id}/result", headers=dept_head_token_headers
    )

    assert response.status_code == 200
    data = response.json()
    final_eval_data = data["final_evaluation"]
    assert final_eval_data["evaluatee_id"] == subordinate.id
    assert final_eval_data["grade"] == "S"
    assert final_eval_data["final_score"] == 95.0
    assert final_eval_data["peer_score"] == 92.0
    assert final_eval_data["pm_score"] == 96.0
    assert final_eval_data["qualitative_score"] == 97.0
    
    assert len(data["peer_feedback"]) == 1
    assert data["peer_feedback"][0] == "Great team player!"


def test_read_subordinate_evaluation_unauthorized_role(
    client: TestClient, db: Session
) -> None:
    # Create two regular users
    user1 = create_random_user(db, role=UserRole.EMPLOYEE)
    user2 = create_random_user(db, role=UserRole.EMPLOYEE)

    # Get token for user1 and try to access user2's data
    user1_token_headers = authentication_token_from_username(
        client=client, username=user1.username, db=db
    )
    response = client.get(
        f"{settings.API_V1_STR}/evaluations/{user2.id}/result", headers=user1_token_headers
    )

    assert response.status_code == 403
    assert "Not enough privileges" in response.json()["detail"]


def test_read_subordinate_evaluation_dept_head_for_other_dept(
    client: TestClient, db: Session
) -> None:
    # Create a dept_head and a user in a different department
    org1 = create_random_organization(db)
    org2 = create_random_organization(db)
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org1.id)
    other_user = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=org2.id)

    # Get token for dept_head and try to access other_user's data
    dept_head_token_headers = authentication_token_from_username(
        client=client, username=dept_head.username, db=db
    )
    response = client.get(
        f"{settings.API_V1_STR}/evaluations/{other_user.id}/result", headers=dept_head_token_headers
    )

    assert response.status_code == 403
    assert "Not enough privileges" in response.json()["detail"]

def test_read_subordinate_evaluation_as_admin(
    client: TestClient, db: Session
) -> None:
    # Create an admin and a regular user
    admin = create_random_user(db, role=UserRole.ADMIN)
    user = create_random_user(db, role=UserRole.EMPLOYEE)

    # Create evaluation data for the user
    today = datetime.date.today()
    period = f"{today.year}-H{1 if today.month <= 6 else 2}"
    crud.final_evaluation.create(
        db,
        obj_in=FinalEvaluationCreate(
            evaluatee_id=user.id,
            evaluation_period=period,
            final_score=75.0,
            grade="B",
        ),
    )

    # Get admin token and make request
    admin_token_headers = authentication_token_from_username(
        client=client, username=admin.username, db=db
    )
    response = client.get(
        f"{settings.API_V1_STR}/evaluations/{user.id}/result", headers=admin_token_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["final_evaluation"]["evaluatee_id"] == user.id
    assert data["final_evaluation"]["grade"] == "B"
