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


def test_read_qualitative_evaluations(client: TestClient, db: Session) -> None:
    # 1. Setup
    # Orgs
    dept_org = create_random_organization(db, name="Department")
    team_org = create_random_organization(db, parent_id=dept_org.id, name="Team 1")
    
    # Users
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=dept_org.id)
    team_lead = create_random_user(db, role=UserRole.TEAM_LEAD, organization_id=team_org.id, reports_to=dept_head.id)
    employee1 = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=team_org.id, reports_to=team_lead.id)
    employee2 = create_random_user(db, role=UserRole.EMPLOYEE, organization_id=team_org.id, reports_to=team_lead.id)
    
    # Active Period
    create_random_evaluation_period(db, start_date=datetime.date.today() - datetime.timedelta(days=1), end_date=datetime.date.today() + datetime.timedelta(days=1))

    # Pre-existing evaluation data from team_lead to employee1
    team_lead_headers = authentication_token_from_username(client=client, username=team_lead.username, db=db)
    client.post(
        f"{settings.API_V1_STR}/evaluations/qualitative-evaluations/",
        headers=team_lead_headers,
        json={
            "evaluations": [{
                "evaluatee_id": employee1.id,
                "qualitative_score": 15,
                "department_contribution_score": 7,
                "feedback": "Good progress"
            }]
        }
    )

    # 2. Test as DEPT_HEAD
    dept_head_headers = authentication_token_from_username(client=client, username=dept_head.username, db=db)
    response_dept_head = client.get(f"{settings.API_V1_STR}/evaluations/qualitative-evaluations/", headers=dept_head_headers)
    
    assert response_dept_head.status_code == 200
    data_dept_head = response_dept_head.json()
    # Dept head should only see the team lead to evaluate
    assert len(data_dept_head["members_to_evaluate"]) == 1
    assert data_dept_head["members_to_evaluate"][0]["evaluatee_id"] == team_lead.id
    assert data_dept_head["status"] == "NOT_STARTED" # No evaluation submitted yet

    # 3. Test as TEAM_LEAD
    response_team_lead = client.get(f"{settings.API_V1_STR}/evaluations/qualitative-evaluations/", headers=team_lead_headers)
    
    assert response_team_lead.status_code == 200
    data_team_lead = response_team_lead.json()
    # Team lead should see both employees
    assert len(data_team_lead["members_to_evaluate"]) == 2
    
    # Check status is IN_PROGRESS since one is evaluated
    assert data_team_lead["status"] == "IN_PROGRESS"
    
    # Verify the pre-existing data for employee1
    eval_for_emp1 = next((m for m in data_team_lead["members_to_evaluate"] if m["evaluatee_id"] == employee1.id), None)
    assert eval_for_emp1 is not None
    assert eval_for_emp1["qualitative_score"] == 15
    assert eval_for_emp1["department_contribution_score"] == 7
    assert eval_for_emp1["feedback"] == "Good progress"
    
    # Verify employee2 has no data yet
    eval_for_emp2 = next((m for m in data_team_lead["members_to_evaluate"] if m["evaluatee_id"] == employee2.id), None)
    assert eval_for_emp2 is not None
    assert eval_for_emp2["qualitative_score"] is None
    assert eval_for_emp2["department_contribution_score"] is None
    assert eval_for_emp2["feedback"] is None


