from unittest.mock import MagicMock
from app.crud import organization as org_crud
from app.schemas.organization import OrganizationCreate
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
    result = org_crud.create_organization(db=mock_db, org=org_in)

    # Assert
    assert result is not None
    assert isinstance(result, Organization)
    assert result.name == org_in.name
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
