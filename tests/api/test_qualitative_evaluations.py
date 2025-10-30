from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import UserRole
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.organization import create_random_organization
from tests.utils.evaluation import create_random_evaluation_period
import datetime

def test_create_qualitative_evaluations_success(client: TestClient, db: Session) -> None:
    # Create a department head and a team member in the same organization
    org = create_random_organization(db)
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org.id)
    team_member = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=org.id)
    create_random_evaluation_period(db, start_date=datetime.date.today() - datetime.timedelta(days=1), end_date=datetime.date.today() + datetime.timedelta(days=1))


    # Log in as the department head
    headers = authentication_token_from_username(client=client, username=dept_head.username, db=db)

    data = {
        "evaluations": [
            {
                "evaluatee_id": team_member.id, 
                "qualitative_score": 18, 
                "department_contribution_score": 9,
                "feedback": "Exceeded expectations on all fronts."
            }
        ]
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/qualitative-evaluations/", headers=headers, json=data)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert content[0]["qualitative_score"] == 18
    assert content[0]["department_contribution_score"] == 9
    assert content[0]["feedback"] == "Exceeded expectations on all fronts."
    assert content[0]["evaluator_id"] == dept_head.id

def test_create_qualitative_evaluations_not_a_manager(client: TestClient, db: Session) -> None:
    # Create an employee and another employee to evaluate
    org = create_random_organization(db)
    evaluator = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=org.id)
    evaluatee = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=org.id)
    create_random_evaluation_period(db, start_date=datetime.date.today() - datetime.timedelta(days=1), end_date=datetime.date.today() + datetime.timedelta(days=1))

    # Log in as the evaluator
    headers = authentication_token_from_username(client=client, username=evaluator.username, db=db)

    data = {
        "evaluations": [
            {
                "evaluatee_id": evaluatee.id, 
                "qualitative_score": 15,
                "department_contribution_score": 7
            }
        ]
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/qualitative-evaluations/", headers=headers, json=data)
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "User does not have the right to perform qualitative evaluations."

def test_create_qualitative_evaluations_not_a_subordinate(client: TestClient, db: Session) -> None:
    # Create a department head and a team member in different organizations
    org1 = create_random_organization(db)
    org2 = create_random_organization(db)
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org1.id)
    team_member = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=org2.id)
    create_random_evaluation_period(db, start_date=datetime.date.today() - datetime.timedelta(days=1), end_date=datetime.date.today() + datetime.timedelta(days=1))

    # Log in as the department head
    headers = authentication_token_from_username(client=client, username=dept_head.username, db=db)

    data = {
        "evaluations": [
            {
                "evaluatee_id": team_member.id, 
                "qualitative_score": 15,
                "department_contribution_score": 7
            }
        ]
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/qualitative-evaluations/", headers=headers, json=data)
    assert response.status_code == 403
    content = response.json()
    assert f"User {team_member.id} is not a subordinate of the evaluator." in content["detail"]

def test_create_qualitative_evaluations_score_out_of_range(client: TestClient, db: Session) -> None:
    # Create a department head and a team member in the same organization
    org = create_random_organization(db)
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org.id)
    team_member = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=org.id)
    create_random_evaluation_period(db, start_date=datetime.date.today() - datetime.timedelta(days=1), end_date=datetime.date.today() + datetime.timedelta(days=1))

    # Log in as the department head
    headers = authentication_token_from_username(client=client, username=dept_head.username, db=db)

    data = {
        "evaluations": [
            {
                "evaluatee_id": team_member.id, 
                "qualitative_score": 21, # > 20, invalid
                "department_contribution_score": 5
            }
        ]
    }
    response = client.post(f"{settings.API_V1_STR}/evaluations/qualitative-evaluations/", headers=headers, json=data)
    assert response.status_code == 422 # Pydantic validation error
    content = response.json()
    assert "Input should be less than or equal to 20" in content["detail"][0]["msg"]

