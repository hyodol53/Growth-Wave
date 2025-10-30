from typing import Dict, List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import datetime

from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserRole
from app.schemas.evaluation import EvaluationItem, FinalEvaluationCalculateRequest
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.organization import create_random_organization
from tests.utils.project import create_random_project
from tests.utils.project_member import create_project_member
from tests.utils.evaluation import create_random_evaluation_weight, create_random_peer_evaluation, create_random_pm_evaluation, create_random_qualitative_evaluation, create_random_evaluation_period


def test_calculate_final_evaluations_as_dept_head(
    client: TestClient, db: Session
) -> None:
    # 1. Setup: Create users, orgs, projects, weights, and evaluations
    # Users and Orgs
    org = create_random_organization(db)
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org.id)
    team_lead = create_random_user(db, organization_id=org.id)
    employee1 = create_random_user(db, organization_id=org.id)
    employee2 = create_random_user(db, organization_id=org.id)
    
    dept_head_headers = authentication_token_from_username(
        client=client, username=dept_head.username, db=db
    )

    # Projects
    project1 = create_random_project(db, pm_id=team_lead.id)
    project2 = create_random_project(db, pm_id=team_lead.id)
    # Define a consistent evaluation period for the test
    test_evaluation_period = f"{datetime.date.today().year}-H{1 if datetime.date.today().month <= 6 else 2}"
    create_random_evaluation_period(db, name=test_evaluation_period)

    # Project Members (employee1 is in two projects)
    create_project_member(db, project_id=project1.id, user_id=employee1.id, participation_weight=60.0)
    create_project_member(db, project_id=project2.id, user_id=employee1.id, participation_weight=40.0)
    create_project_member(db, project_id=project1.id, user_id=employee2.id, participation_weight=100.0)
    create_project_member(db, project_id=project1.id, user_id=team_lead.id, is_pm=True)


    # Evaluation Weights for EMPLOYEE role (used for project score component)
    create_random_evaluation_weight(db, role=UserRole.EMPLOYEE, item=EvaluationItem.PEER_REVIEW, weight=30.0)
    create_random_evaluation_weight(db, role=UserRole.EMPLOYEE, item=EvaluationItem.PM_REVIEW, weight=50.0)
    # This weight is no longer used in the final calculation, but we leave it for completeness
    create_random_evaluation_weight(db, role=UserRole.EMPLOYEE, item=EvaluationItem.QUALITATIVE_REVIEW, weight=20.0)

    # Evaluations for employee1
    # Project 1
    create_random_peer_evaluation(db, evaluator_id=team_lead.id, evaluatee_id=employee1.id, project_id=project1.id, score=80, evaluation_period=test_evaluation_period)
    create_random_pm_evaluation(db, evaluator_id=team_lead.id, evaluatee_id=employee1.id, project_id=project1.id, score=90, evaluation_period=test_evaluation_period)
    # Project 2
    create_random_peer_evaluation(db, evaluator_id=team_lead.id, evaluatee_id=employee1.id, project_id=project2.id, score=70, evaluation_period=test_evaluation_period)
    create_random_pm_evaluation(db, evaluator_id=team_lead.id, evaluatee_id=employee1.id, project_id=project2.id, score=85, evaluation_period=test_evaluation_period)
    # Qualitative
    create_random_qualitative_evaluation(
        db, evaluator_id=dept_head.id, evaluatee_id=employee1.id, 
        qualitative_score=18, department_contribution_score=9, 
        evaluation_period=test_evaluation_period
    )

    # 2. Action: Trigger calculation
    response = client.post(
        f"{settings.API_V1_STR}/evaluations/calculate",
        headers=dept_head_headers,
        json=FinalEvaluationCalculateRequest(user_ids=[employee1.id]).model_dump()
    )
    
    # 3. Assert
    assert response.status_code == 200
    final_evals = response.json()
    assert len(final_evals) == 1
    
    final_eval = final_evals[0]
    assert final_eval["evaluatee_id"] == employee1.id
    
    # Expected calculation for employee1 with new 70/30 logic
    # Peer Score: (80 * 0.6) + (70 * 0.4) = 48 + 28 = 76
    # PM Score: (90 * 0.6) + (85 * 0.4) = 54 + 34 = 88
    # Project Score Component:
    #   - Weights: Peer=30, PM=50. Total=80.
    #   - Normalized: Peer=30/80=0.375, PM=50/80=0.625
    #   - Project Score = (76 * 0.375) + (88 * 0.625) = 28.5 + 55 = 83.5
    # Qualitative Score Component:
    #   - Combined Score = 18 + 9 = 27
    #   - Normalized Score = (27 / 30) * 100 = 90
    # Final Score = (Project Score * 0.7) + (Qualitative Normalized Score * 0.3)
    #             = (83.5 * 0.7) + (90 * 0.3) = 58.45 + 27 = 85.45
    assert final_eval["peer_score"] == 76.0
    assert final_eval["pm_score"] == 88.0
    assert final_eval["qualitative_score"] == 27.0 # Combined score
    assert round(final_eval["final_score"], 2) == 85.45

def test_calculate_final_evaluations_for_pm(
    client: TestClient, db: Session
) -> None:
    # 1. Setup
    admin_user = create_random_user(db, role=UserRole.ADMIN)
    org = create_random_organization(db)
    dept_head = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org.id)
    pm_user = create_random_user(db, role=UserRole.TEAM_LEAD, organization_id=org.id)
    
    admin_headers = authentication_token_from_username(client=client, username=admin_user.username, db=db)

    project = create_random_project(db, pm_id=pm_user.id)
    test_evaluation_period = f"{datetime.date.today().year}-H{1 if datetime.date.today().month <= 6 else 2}"
    create_random_evaluation_period(db, name=test_evaluation_period)

    create_project_member(db, project_id=project.id, user_id=pm_user.id, participation_weight=100.0, is_pm=True)

    # Evaluation Weights for TEAM_LEAD role
    create_random_evaluation_weight(db, role=UserRole.TEAM_LEAD, item=EvaluationItem.PEER_REVIEW, weight=40.0)
    create_random_evaluation_weight(db, role=UserRole.TEAM_LEAD, item=EvaluationItem.PM_REVIEW, weight=40.0)
    create_random_evaluation_weight(db, role=UserRole.TEAM_LEAD, item=EvaluationItem.QUALITATIVE_REVIEW, weight=20.0)

    # Admin enters the PM's own evaluation score
    pm_self_eval_data = {"project_id": project.id, "evaluatee_id": pm_user.id, "score": 98}
    response = client.post(f"{settings.API_V1_STR}/evaluations/pm-self-evaluation/", headers=admin_headers, json=pm_self_eval_data)
    assert response.status_code == 200

    # Other evaluations for the PM
    create_random_peer_evaluation(db, evaluator_id=dept_head.id, evaluatee_id=pm_user.id, project_id=project.id, score=85, evaluation_period=test_evaluation_period)
    create_random_qualitative_evaluation(
        db, evaluator_id=dept_head.id, evaluatee_id=pm_user.id, 
        qualitative_score=18, department_contribution_score=8, 
        evaluation_period=test_evaluation_period
    )

    # 2. Action: Trigger calculation for the PM
    calc_response = client.post(
        f"{settings.API_V1_STR}/evaluations/calculate",
        headers=admin_headers,
        json=FinalEvaluationCalculateRequest(user_ids=[pm_user.id]).model_dump()
    )

    # 3. Assert
    assert calc_response.status_code == 200
    final_evals = calc_response.json()
    assert len(final_evals) == 1
    final_eval = final_evals[0]

    # Expected calculation for PM with new 70/30 logic
    # Peer Score: 85
    # PM Score: 98
    # Project Score Component:
    #   - Weights: Peer=40, PM=40. Total=80.
    #   - Normalized: Peer=40/80=0.5, PM=40/80=0.5
    #   - Project Score = (85 * 0.5) + (98 * 0.5) = 42.5 + 49 = 91.5
    # Qualitative Score Component:
    #   - Combined Score = 18 + 8 = 26
    #   - Normalized Score = (26 / 30) * 100 = 86.67
    # Final Score = (Project Score * 0.7) + (Qualitative Normalized Score * 0.3)
    #             = (91.5 * 0.7) + (86.666... * 0.3) = 64.05 + 26 = 90.05
    assert final_eval["evaluatee_id"] == pm_user.id
    assert final_eval["peer_score"] == 85.0
    assert final_eval["pm_score"] == 98.0
    assert final_eval["qualitative_score"] == 26.0 # Combined score
    assert round(final_eval["final_score"], 2) == 90.05


def test_calculate_final_evaluations_unauthorized(
    client: TestClient, db: Session
) -> None:
    # 1. Setup
    employee = create_random_user(db, role=UserRole.EMPLOYEE)
    employee_headers = authentication_token_from_username(
        client=client, username=employee.username, db=db
    )

    # 2. Action
    response = client.post(
        f"{settings.API_V1_STR}/evaluations/calculate",
        headers=employee_headers,
        json=FinalEvaluationCalculateRequest(user_ids=[employee.id]).model_dump()
    )

    # 3. Assert
    assert response.status_code == 403
    assert "Not enough privileges" in response.json()["detail"]