from unittest.mock import MagicMock
import pytest
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app import crud
from app.models.user import UserRole
from app.models.evaluation import FinalEvaluation
from app.schemas.organization import OrganizationCreate
from app.schemas.user import UserCreate
from app.schemas.evaluation import EvaluationPeriodCreate
from app.models.organization import Organization


def test_create_organization_returns_object():
    """
    Tests that the create_organization CRUD function returns the created object.
    This would have caught the previously missed return statement.
    """
    # Arrange
    mock_db = MagicMock()
    org_in = OrganizationCreate(name="Test Org", level=1, parent_id=None)

    # Act
    result = crud.organization.create_organization(db=mock_db, org=org_in)

    # Assert
    assert result is not None
    assert isinstance(result, Organization)
    assert result.name == org_in.name
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_set_department_grade_syncs_to_dept_head(db: Session) -> None:
    """
    Tests that setting a department's grade correctly syncs to the
    department head's final evaluation record.
    """
    # 1. GIVEN: Setup the necessary data
    # Create an active evaluation period
    period_in = EvaluationPeriodCreate(
        name="Test Period 2025 H2",
        start_date=date.today() - timedelta(days=30),
        end_date=date.today() + timedelta(days=30),
    )
    active_period = crud.evaluation_period.create(db, obj_in=period_in)

    # Create an organization (department)
    org_in = OrganizationCreate(name="R&D Team 1", level=2)
    department = crud.organization.create_organization(db, org=org_in)

    # Create a department head for that organization
    dept_head_in = UserCreate(
        username="depthead01",
        email="depthead01@test.com",
        password="password",
        full_name="John Doe",
        role=UserRole.DEPT_HEAD,
        organization_id=department.id,
    )
    dept_head = crud.user.user.create(db, obj_in=dept_head_in)

    # 2. WHEN: The department grade is set
    updated_org = crud.organization.set_department_grade(db, db_org=department, grade="S")

    # 3. THEN: The changes should be reflected in the DB
    # Check if the organization's grade is updated
    assert updated_org.department_grade == "S"
    db.refresh(department)
    assert department.department_grade == "S"

    # Check if the final evaluation for the dept head is created and correct
    final_eval = (
        db.query(FinalEvaluation)
        .filter(
            FinalEvaluation.evaluatee_id == dept_head.id,
            FinalEvaluation.evaluation_period == active_period.name,
        )
        .first()
    )
    assert final_eval is not None
    assert final_eval.grade == "S"
