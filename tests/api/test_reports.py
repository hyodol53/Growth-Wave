from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.user import UserRole
from tests.utils.user import create_random_user, authentication_token_from_username
from tests.utils.organization import create_random_organization
from tests.utils.praise import create_random_praise

def test_get_growth_culture_report_as_dept_head(client: TestClient, db: Session) -> None:
    # 1. Create users and organizations
    # - A department head (manager)
    # - An employee in the same department
    # - An employee in a different department
    org1 = create_random_organization(db)
    org2 = create_random_organization(db)
    manager = create_random_user(db, role=UserRole.DEPT_HEAD, organization_id=org1.id)
    employee_in_dept = create_random_user(db, organization_id=org1.id)
    employee_other_dept = create_random_user(db, organization_id=org2.id)

    # 2. Create praise data for the employee to generate a strength profile
    praiser = create_random_user(db)
    create_random_praise(db, sender=praiser, recipient=employee_in_dept, hashtags=["#teamwork", "#problem-solver"])
    create_random_praise(db, sender=praiser, recipient=employee_in_dept, hashtags=["#teamwork"])

    # 3. Authenticate as the department head
    headers = authentication_token_from_username(client=client, username=manager.username, db=db)

    # 4. Request the report for the employee in the same department (should succeed)
    response = client.get(f"{settings.API_V1_STR}/users/{employee_in_dept.id}/growth-culture-report", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "strength_profile" in data
    assert data["strength_profile"]["total_praises"] == 2
    assert len(data["strength_profile"]["strengths"]) == 2
    # Check if strengths are sorted correctly by count
    assert data["strength_profile"]["strengths"][0]["hashtag"] == "#teamwork"
    assert data["strength_profile"]["strengths"][0]["count"] == 2

    # 5. Request the report for the employee in another department (should fail)
    response = client.get(f"{settings.API_V1_STR}/users/{employee_other_dept.id}/growth-culture-report", headers=headers)
    assert response.status_code == 403
    assert "only view reports for users in your department" in response.json()["detail"]

# def test_get_growth_culture_report_unauthorized_role(client: TestClient, db: Session) -> None:
#     # 1. Create users
#     employee = create_random_user(db, role=UserRole.EMPLOYEE)
#     target_user = create_random_user(db)

#     # 2. Authenticate as the employee
#     headers = authentication_token_from_username(client=client, username=employee.username, db=db)

#     # 3. Request the report (should fail with 403)
#     response = client.get(f"{settings.API_V1_STR}/users/{target_user.id}/growth-culture-report", headers=headers)
#     assert response.status_code == 403
#     assert "not have enough privileges" in response.json()["detail"]
